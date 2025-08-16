from django.urls import path, include

app_name = "partials"
urlpatterns = [
    path(
        "actions/",
        include("professions.dashboard.partials.actions.urls", namespace="actions"),
    )
]
