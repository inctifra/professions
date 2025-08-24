from django.conf import settings
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin

from .models import SiteConfig


class MaintenanceModeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == "/waitlist/" and request.method == "POST":
            return None
        if settings.DEBUG and request.path.startswith("/__reload__/"):
            return None
        config = SiteConfig.get_solo()
        if config.maintenance_mode and not request.user.is_staff:
            return render(request, "maintenance.html", status=503)
        return None
