from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Pharmacy
from .models import Pharmtech
from .serializers import PharmacySerializer
from .serializers import PharmtechSerializer
from .throttles import PharmacyThrottle, PharmtechThrottle
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    list=extend_schema(
        tags=["Professions - Pharmacies"],
        description="""
        Returns a list of all registered pharmacy professionals.
        You can use query parameters to filter the results.""",
    ),
    retrieve=extend_schema(
        tags=["Professions - Pharmacies"],
        description="""
        Returns detailed information about a specific registered pharmacy
        professional based on their ID.""",
    ),
)
class PharmacyViewSet(ReadOnlyModelViewSet):
    queryset = Pharmacy.objects.using("cloud_readonly").all()
    serializer_class = PharmacySerializer
    throttle_classes = [PharmacyThrottle]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "registration_number"]
    search_fields = ["name", "license_number"]
    ordering_fields = ["valid_till", "name"]


@extend_schema_view(
    list=extend_schema(tags=["Professions - Pharmacy Technicians"]),
    retrieve=extend_schema(tags=["Professions - Pharmacy Technician"]),
)
class PharmtechViewSet(ReadOnlyModelViewSet):
    queryset = Pharmtech.objects.using("cloud_readonly").all()
    serializer_class = PharmtechSerializer
    throttle_classes = [PharmtechThrottle]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "registration_number"]
    search_fields = ["name", "license_number"]
    ordering_fields = ["valid_till", "name"]
