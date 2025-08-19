from django.urls import include
from django.urls import path

from apps.dashboard import views

app_name = "dashboard"
urlpatterns = [
    path("", views.dashboard, name="home"),
    path("domains/", views.domains_view, name="domains"),
    path("api-keys/", views.api_keys_view, name="apikeys"),
    path("api/", include("apps.dashboard.api_router")),
    path("plans/", include("apps.plans.urls", namespace="plans")),
    path("projects/", include("apps.projects.urls", namespace="projects")),
    path("users/", include("professions.users.urls", namespace="users")),
    path(
        "partials/",
        include("apps.dashboard.partials.urls", namespace="partials"),
    ),
]
