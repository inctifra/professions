import time
from http import HTTPStatus

from rest_framework.exceptions import PermissionDenied

from apps.analytics.tasks import revoke_and_update_api_key_attempts
from apps.analytics.tasks import unrevoke_and_update_api_key_attempts
from apps.professions_reader.constants import MAX_INVALID_DOMAIN_REQUEST_COUNT


class APIKeyValidationMixin:
    """
    Handles API key revocation, invalid domain attempts, and request start time.
    """

    def initial(self, request, *args, **kwargs):
        request._start_time = time.time()  # noqa: SLF001

        api_key = getattr(request.user, "api_key", None)
        project = getattr(request.user, "project", None)
        domain = getattr(request.user, "domain", None)
        invalid_domain_name = getattr(request, "invalid_domain_name", None)

        if project:
            request._project_id = str(project.uuid)  # noqa: SLF001
        elif domain:
            request._project_id = str(domain.project.uuid)  # noqa: SLF001
        else:
            request._project_id = None  # noqa: SLF001

        if api_key and (
            api_key.failed_domain_attempts > MAX_INVALID_DOMAIN_REQUEST_COUNT):
            self._log_api_entry(
                request,
                status_code=HTTPStatus.FORBIDDEN,
                error_message="Your API key has been revoked.",
                api_key_id=api_key.key_id,
            )
            msg = "Your API key has been revoked."
            raise PermissionDenied(msg)

        if invalid_domain_name and (
            api_key.failed_domain_attempts < MAX_INVALID_DOMAIN_REQUEST_COUNT):
            revoke_and_update_api_key_attempts.delay(api_key.key_id)
            self._log_api_entry(
                request,
                status_code=HTTPStatus.FORBIDDEN,
                error_message=f"API key not allowed from domain: {invalid_domain_name}",
                api_key_id=api_key.key_id,
            )
            msg = f"API key not allowed from domain: {invalid_domain_name}"
            raise PermissionDenied(msg)

        if api_key and api_key.status == (
            "revoked" and not getattr(request, "invalid_domain_name", None)):
            unrevoke_and_update_api_key_attempts.delay(api_key.key_id)

        return super().initial(request, *args, **kwargs)
