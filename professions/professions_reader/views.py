from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Accountant
from .models import Pharmacy
from .models import Pharmtech, Advocates
from .serializers import AccountantSerializer
from .serializers import PharmacySerializer
from .serializers import PharmtechSerializer, AdvocateSerializer
from .throttles import PharmacyThrottle
from .throttles import PharmtechThrottle


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


@extend_schema_view(
    list=extend_schema(tags=["Accountants - The registered accounts of kenya"]),
    retrieve=extend_schema(tags=["Accountant - The accountant detail"]),
)
class AccountantViewSet(ReadOnlyModelViewSet):
    queryset = Accountant.objects.using("cloud_readonly").all()
    serializer_class = AccountantSerializer
    throttle_classes = []
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fields = ["-timestamp"]


@extend_schema_view(
    list=extend_schema(tags=["Advocates - The registered advocates of kenya"]),
    retrieve=extend_schema(tags=["Advocate - The advocate detail"]),
)
class AdvocateViewSet(ReadOnlyModelViewSet):
    queryset = Advocates.objects.using("cloud_readonly").all()
    serializer_class = AdvocateSerializer
    throttle_classes = []
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fields = ["-timestamp"]

