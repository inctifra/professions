from django.urls import path, include

urlpatterns = [
    path("", include("apps.core.urls")),
    path("dashboard/", include("apps.dashboard.urls", namespace="dashboard")),
]
