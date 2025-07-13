from django.urls import include
from django.urls import path
from django.views.generic.base import TemplateView

from .views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("api/", include("professions.core.api.urls")),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path(
        "docs/",
        TemplateView.as_view(template_name="pages/professions.html"),
        name="docs",
    ),
]
