from django.urls import path

from .views import delete_api_key_view
from .views import delete_domain_view

app_name = "actions"
urlpatterns = [
    path("<api_key_id>/", view=delete_api_key_view, name="delete_api_key"),
    path("domains/<domain_id>/delete", view=delete_domain_view, name="delete_domain"),
]
