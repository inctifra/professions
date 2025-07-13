from django.urls import path

from . import views

urlpatterns = [
    path("contacts/", views.ContactListAPIView.as_view()),
    path("search/", views.ProfessionalLookupAPIView.as_view()),
]
