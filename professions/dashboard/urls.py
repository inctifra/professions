from django.urls import include
from django.urls import path

from professions.dashboard import views

app_name = "dashboard"
urlpatterns = [
    path("", views.dashboard, name="home"),
    path("domains/", views.domains_view, name="domains"),
    path("api-keys/", views.api_keys_view, name="apikeys"),
    path("api/", include("professions.dashboard.api_router")),
    path("plans/", include("professions.plans.urls", namespace="plans")),
    path("projects/", include("professions.projects.urls", namespace="projects")),
    path("users/", include("professions.users.urls", namespace="users")),
    path(
        "partials/",
        include("professions.dashboard.partials.urls", namespace="partials"),
    ),
]
