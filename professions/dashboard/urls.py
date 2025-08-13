from django.urls import include
from django.urls import path

from professions.dashboard import views

app_name = "dashboard"
urlpatterns = [
    path("", views.dashboard, name="home"),
    path("api/", include("professions.dashboard.api_router")),
    path("plans/", include("professions.plans.urls", namespace="plans")),
]
