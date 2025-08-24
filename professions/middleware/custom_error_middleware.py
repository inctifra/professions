from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import APIException


class APIExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        # Apply only to /api/ paths
        if not request.path.startswith("/api/"):
            return None

        # Skip DRF exceptions (they already produce JSON responses)
        if isinstance(exception, APIException):
            return None

        # Otherwise, return a standard JSON error response
        return JsonResponse(
            {
                "status_code": 500,
                "error": True,
                "message": str(exception),
                "path": request.path,
            },
            status=500,
        )
