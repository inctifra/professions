from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from professions.professions_reader.versions.v1.viewsets import AccountantVersionViewSet
from professions.professions_reader.versions.v1.viewsets import AdvocateVersionViewSet
from professions.professions_reader.versions.v1.viewsets import PharmacyVersionViewSet
from professions.professions_reader.versions.v1.viewsets import PharmtechVersionViewSet

router_v1 = DefaultRouter()
router_v1.register("pharmacists", PharmacyVersionViewSet, basename="pharmacy-v1")
router_v1.register(
    "pharmacytechnicians", PharmtechVersionViewSet, basename="pharmtech-v1"
)
router_v1.register("accountants", AccountantVersionViewSet, basename="accountant-v1")
router_v1.register("advocates", AdvocateVersionViewSet, basename="advocate-v1")

urlpatterns = [
    path("", include(router_v1.urls)),
]
