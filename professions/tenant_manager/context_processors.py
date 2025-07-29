from django.http.request import HttpRequest


def load_tenant_manager(request: HttpRequest) -> dict:
    """
    Middleware to ensure that the tenant manager is loaded for each request.
    This is necessary for handling tenant-specific logic in the application.
    """
    scheme = (request.is_secure() and "https") or "http"
    return {
        "dashboard_url": f"{scheme}://dashboard.{request.get_host()}",
    }
