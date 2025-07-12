from rest_framework import status
from rest_framework.exceptions import Throttled
from rest_framework.response import Response
from rest_framework.views import exception_handler


def throttling_exception_handler(exc, context):
    if isinstance(exc, Throttled):
        return Response(
            {
                "detail": "Request was throttled.",
                "available_in": exc.wait,
                "throttle_scope": getattr(exc, "throttle_scope", "unknown"),
            },
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    return exception_handler(exc, context)
