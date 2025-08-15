from django.conf import settings
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from professions.professions_reader.resources import list_api_resources
from professions.users.api.views import UserRegisterView
from professions.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)

app_name = "api"
urlpatterns = [
    path("users/signup/", UserRegisterView.as_view()),
    path("professions/", include("professions.professions_reader.urls")),
    path("v1/professions/", include("professions.professions_reader.versions.urls")),
    path("resources/", list_api_resources, name="resources"),
    *router.urls,
]
