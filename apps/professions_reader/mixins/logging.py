import logging
import time
from http import HTTPStatus

from rest_framework.request import Request
from rest_framework.response import Response

from apps.analytics.tasks import log_api_request

logger = logging.getLogger(__file__)


class APILoggingMixin:
    """
    Handles API request logging for both success and error cases.
    """

    def _log_api_entry(self, request, status_code, error_message="", api_key_id=None):
        elapsed_ms = int(
            (time.time() - getattr(request, "_start_time", time.time())) * 1000)
        project_id = getattr(request, "_project_id", None)

        log_api_request.delay(
            {
                "api_key_id": api_key_id,
                "project_id": project_id,
                "endpoint": request.path,
                "method": request.method,
                "status_code": status_code,
                "response_time_ms": elapsed_ms,
                "ip_address": request.META.get("REMOTE_ADDR", ""),
                "user_agent": request.META.get("HTTP_USER_AGENT", ""),
                "error_message": error_message,
            },
        )

    def _log_success_api_entry(self, request: Request,
                               response: Response, *args, **kwargs):
        start_time = getattr(request, "_start_time", None)
        elapsed_ms = int((time.time() - start_time) * 1000) if start_time else 0
        api_key = None
        logger.info("Elapsed time: %d", elapsed_ms)

        if HTTPStatus.OK < response.status_code < HTTPStatus.MULTIPLE_CHOICES:
            if hasattr(request, "user") and hasattr(request.user, "api_key"):
                api_key = request.user.api_key
            self._log_api_entry(request, status_code=response.status_code, api_key_id=api_key.key_id)
        else:
            api_key_id = getattr(getattr(request, "user", None), "api_key", None)
            api_key_id = api_key_id.key_id if api_key_id else None
            self._log_api_entry(
                request,
                status_code=response.status_code,
                error_message=getattr(request, "_error_message", ""),
                api_key_id=api_key_id,
            )

    def finalize_response(self, request, response, *args, **kwargs):
        self._log_success_api_entry(request, response, *args, **kwargs)
        return super().finalize_response(request, response, *args, **kwargs)
