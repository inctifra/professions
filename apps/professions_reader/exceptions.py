import time

from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import Throttled
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from apps.analytics.tasks import log_api_request


def __throttling_exception_handler(exc, context):
    if isinstance(exc, Throttled):
        return Response(
            {
                "detail": "Request was throttled.",
                "available_in": exc.wait,
                "throttle_scope": getattr(exc, "throttle_scope", "unknown"),
            },
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    return drf_exception_handler(exc, context)


def master_exception_handler(exc, context):
    """
    Master exception handler that combines throttling and custom API key/domain errors.
    """
    # --- Default DRF exception handler ---
    response = drf_exception_handler(exc, context)
    #  --- Handle Error Logging ---
    request = context.get("request")
    api_key_id = None
    project_id = None
    error_message = str(exc)

    if request and hasattr(request, "user") and hasattr(request.user, "api_key"):
        api_key_id = request.user.api_key.key_id
        project = getattr(request.user, "project", None)
        domain = getattr(request.user, "domain", None)

        if project:
            project_id = str(project.uuid)
        elif domain:
            project_id = domain.project.uuid

    if request:
        start_time = getattr(request, "_start_time", None)
        elapsed_ms = int((time.time() - start_time) * 1000) if start_time else 0
        log_api_request.delay(
            {
                "api_key_id": api_key_id,
                "project_id": project_id,
                "endpoint": request.path,
                "method": request.method,
                "status_code": getattr(response, "status_code", 500),
                "response_time_ms": elapsed_ms,
                "ip_address": request.META.get("REMOTE_ADDR", ""),
                "user_agent": request.META.get("HTTP_USER_AGENT", ""),
                "error_message": error_message,
            }
        )

    # --- Handle throttling first via your existing handler ---
    if isinstance(exc, Throttled):
        return __throttling_exception_handler(exc, context)

    # --- Handle PermissionDenied with descriptive message ---
    if isinstance(exc, PermissionDenied):
        # Extract the message from the exception
        detail = getattr(exc, "detail", str(exc))
        return Response(
            {
                "error": detail,
                "type": exc.__class__.__name__,
                "status_code": status.HTTP_403_FORBIDDEN,
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    # Ensure status code is included in JSON if response exists
    if response is not None:
        response.data["status_code"] = response.status_code

    return response
