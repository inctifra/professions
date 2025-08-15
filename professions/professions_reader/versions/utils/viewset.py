import time
from http import HTTPStatus

from django.db.models import Q
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.exceptions import PermissionDenied

from professions.analytics.tasks import (
    log_api_request,
    revoke_and_update_api_key_attempts,
    unrevoke_and_update_api_key_attempts,
)
from professions.professions_reader.constants import MAX_INVALID_DOMAIN_REQUEST_COUNT
from professions.professions_reader.helpers.throttle import ProjectPlanThrottle
from professions.professions_reader.permissions.authentication import APIKeyAuthentication
from professions.professions_reader.permissions.permissions import HasValidAPIKey


class APIKeyReadOnlyViewSet(ReadOnlyModelViewSet):
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [HasValidAPIKey]
    throttle_classes = [ProjectPlanThrottle]
    base_only_fields = ["name"]

    def get_queryset(self):
        qs = super().get_queryset().only(*self.base_only_fields)

        # --- Dynamic search ---
        search = self.request.query_params.get("search")
        if search and hasattr(self, "search_fields"):
            queries = Q()
            for field in self.search_fields:
                queries |= Q(**{f"{field}__icontains": search})
            qs = qs.filter(queries)

        # --- Dynamic filters ---
        if hasattr(self, "filterset_fields"):
            for field in self.filterset_fields:
                value = self.request.query_params.get(field)
                if value is not None:
                    qs = qs.filter(**{field: value})

        # --- Dynamic ordering ---
        ordering = self.request.query_params.get("ordering")
        if ordering and hasattr(self, "ordering_fields"):
            allowed = [
                f.strip()
                for f in ordering.split(",")
                if f.strip() in self.ordering_fields
            ]
            if allowed:
                qs = qs.order_by(*allowed)
        return qs

    def initial(self, request, *args, **kwargs):
        request._start_time = time.time()

        api_key = getattr(request.user, "api_key", None)
        project = getattr(request.user, "project", None)
        domain = getattr(request.user, "domain", None)
        invalid_domain_name = getattr(request, "invalid_domain_name", None)

        # Determine project_id for logging
        if project:
            request._project_id = str(project.uuid)
        elif domain:
            request._project_id = str(domain.project.uuid)
        else:
            request._project_id = None

        # 🚨 Block if API key is revoked due to too many invalid domain attempts
        if api_key and api_key.failed_domain_attempts > MAX_INVALID_DOMAIN_REQUEST_COUNT:
            self._log_api_entry(
                request,
                status_code=HTTPStatus.FORBIDDEN,
                error_message="Your API key has been revoked.",
                api_key_id=api_key.key_id,
            )
            raise PermissionDenied("Your API key has been revoked.")

        # Handle invalid domain attempts
        if invalid_domain_name and api_key.failed_domain_attempts<MAX_INVALID_DOMAIN_REQUEST_COUNT:
            revoke_and_update_api_key_attempts.delay(api_key.key_id)
            self._log_api_entry(
                request,
                status_code=HTTPStatus.FORBIDDEN,
                error_message=f"API key not allowed from domain: {invalid_domain_name}",
                api_key_id=api_key.key_id,
            )
            raise PermissionDenied(f"API key not allowed from domain: {invalid_domain_name}")


        if api_key.status == "revoked" and not getattr(request, "invalid_domain_name", None):
            unrevoke_and_update_api_key_attempts.delay(api_key.key_id)

        return super().initial(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Hook after response is ready to log usage asynchronously.
        """
        self._log_success_api_entry(request, response, *args, **kwargs)
        return super().finalize_response(request, response, *args, **kwargs)

    def _log_api_entry(self, request, status_code, error_message="", api_key_id=None):
        """Shared logging logic for both success and early-deny cases."""
        elapsed_ms = int((time.time() - getattr(request, "_start_time", time.time())) * 1000)
        project_id = getattr(request, "_project_id", "project")
        print("Project ID: ", project_id)

        log_api_request.delay(
            {
                "api_key_id": api_key_id,
                "project_id": getattr(request, "_project_id", None),
                "endpoint": request.path,
                "method": request.method,
                "status_code": status_code,
                "response_time_ms": elapsed_ms,
                "ip_address": request.META.get("REMOTE_ADDR", ""),
                "user_agent": request.META.get("HTTP_USER_AGENT", ""),
                "error_message": error_message,
            }
        )

    def _log_success_api_entry(self, request: Request, response: Response, *args, **kwargs):
        start_time = getattr(request, "_start_time", None)
        elapsed_ms = int((time.time() - start_time) * 1000) if start_time else 0
        api_key = None
        if HTTPStatus.OK < response.status_code < HTTPStatus.MULTIPLE_CHOICES:
            if hasattr(request, "user") and hasattr(request.user, "api_key"):
                api_key = request.user.api_key
            self._log_api_entry(
                request,
                status_code=response.status_code,
                error_message="",
                api_key_id=api_key.key_id,
            )
        else:
            api_key_id = getattr(getattr(request, "user", None), "api_key", None)
            api_key_id = api_key_id.key_id if api_key_id else None
            self._log_api_entry(
                request,
                status_code=response.status_code,
                error_message=getattr(request, "_error_message", ""),
                api_key_id=api_key_id,
            )
