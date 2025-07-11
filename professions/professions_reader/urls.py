from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PharmacyViewSet
from .views import PharmtechViewSet

router = DefaultRouter()
router.register(r"pharmacies", PharmacyViewSet, basename="pharmacy")
router.register(r"pharmtechs", PharmtechViewSet, basename="pharmtech")

urlpatterns = [
    path("", include(router.urls)),
]
