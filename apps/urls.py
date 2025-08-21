from django.urls import include
from django.urls import path

urlpatterns = [
    path("", include("apps.core.urls")),
    path("dashboard/", include("apps.dashboard.urls", namespace="dashboard")),
]
