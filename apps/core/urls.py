from django.urls import include
from django.urls import path
from django.views.generic.base import TemplateView

from .views import HomeView, join_waitlist

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("api/", include("apps.core.api.urls")),
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
    path("waitlist/", join_waitlist, name="join_waitlist"),
]
