from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from professions.users.api.views import UserViewSet
from apps.professions_reader.resources import list_api_resources

from professions.users.api.views import UserRegisterView


router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = [
    path("users/signup/", UserRegisterView.as_view()),
    path("professions/", include("apps.professions_reader.urls")),
    path("v1/professions/", include("apps.professions_reader.versions.urls")),
    path("resources/", list_api_resources, name="resources"),
    path("partials/", include("apps.dashboard.partials.apis.urls")),
    *router.urls,
]

