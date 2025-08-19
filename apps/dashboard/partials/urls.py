from django.urls import include
from django.urls import path

app_name = "partials"
urlpatterns = [
    path(
        "actions/",
        include("apps.dashboard.partials.actions.urls", namespace="actions"),
    ),
]
