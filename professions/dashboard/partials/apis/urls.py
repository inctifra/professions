from django.urls import path
from .views import load_key_for_simulation_view


urlpatterns = [path("keys/", load_key_for_simulation_view)]
