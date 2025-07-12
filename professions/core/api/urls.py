from django.urls import path

from . import views


urlpatterns = [
    path("contacts/", views.ContactListAPIView.as_view()),
]
