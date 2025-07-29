from django.urls import path

from professions.dashboard import views

urlpatterns = [
    path("", views.dashboard, name="home"),
]
