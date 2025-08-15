from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework import filters
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Accountant
from .models import Advocate
from .models import Pharmacy
from .models import Pharmtech
from .serializers import AccountantSerializer
from .serializers import AdvocateSerializer
from .serializers import PharmacySerializer
from .serializers import PharmtechSerializer
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
    base_only_fields = [
        "id",
        "name",
        "registration_number",
        "license_number",
        "status",
        "valid_till",
    ]

    def get_queryset(self):
        qs = Pharmacy.objects.using("cloud_readonly").all().only(*self.base_only_fields)

        search = self.request.query_params.get("search")
        if search:
            queries = Q()
            for field in self.search_fields:
                queries |= Q(**{f"{field}__icontains": search})
            qs = qs.filter(queries)

        for field in self.filterset_fields:
            value = self.request.query_params.get(field)
            if value:
                qs = qs.filter(**{field: value})

        ordering = self.request.query_params.get("ordering")
        if ordering:
            allowed = [
                f.strip()
                for f in ordering.split(",")
                if f.strip() in self.ordering_fields
            ]
            if allowed:
                qs = qs.order_by(*allowed)
        return qs


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
    search_fields = ["name", "memberno"]
    ordering_fields = ["-timestamp"]


@extend_schema_view(
    list=extend_schema(tags=["Advocates - The registered advocates of kenya"]),
    retrieve=extend_schema(tags=["Advocate - The advocate detail"]),
)
class AdvocateViewSet(ReadOnlyModelViewSet):
    queryset = Advocate.objects.using("cloud_readonly").all()
    serializer_class = AdvocateSerializer
    throttle_classes = []
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["name"]
    search_fields = ["name", "advocate_number", "law_firm"]
    ordering_fields = ["-timestamp"]
