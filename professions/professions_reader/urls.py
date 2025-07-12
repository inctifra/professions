from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PharmacyViewSet
from .views import PharmtechViewSet
from .views import AccountantViewSet

router = DefaultRouter()
router.register(r"pharmacists", PharmacyViewSet, basename="pharmacy")
router.register(r"pharmtechs", PharmtechViewSet, basename="pharmtech")
router.register(r"accountants", AccountantViewSet, basename="accountants")

urlpatterns = [
    path("", include(router.urls)),
]
