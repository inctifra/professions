from drf_spectacular.utils import extend_schema

from professions.professions_reader.versions.utils.viewset import APIKeyReadOnlyViewSet
from professions.professions_reader.views import AccountantViewSet
from professions.professions_reader.views import AdvocateViewSet
from professions.professions_reader.views import PharmacyViewSet
from professions.professions_reader.views import PharmtechViewSet


@extend_schema(exclude=True)
class PharmacyVersionViewSet(APIKeyReadOnlyViewSet, PharmacyViewSet):
    """
    Versioned API that uses API key auth and throttling
    """


@extend_schema(exclude=True)
class PharmtechVersionViewSet(APIKeyReadOnlyViewSet, PharmtechViewSet):
    pass


@extend_schema(exclude=True)
class AccountantVersionViewSet(APIKeyReadOnlyViewSet, AccountantViewSet):
    pass


@extend_schema(exclude=True)
class AdvocateVersionViewSet(APIKeyReadOnlyViewSet, AdvocateViewSet):
    pass
