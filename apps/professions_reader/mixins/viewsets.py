import time

from django.core.cache import cache
from django.core.serializers import deserialize
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.professions_reader.mixins.queryset import DynamicQuerysetMixin
from apps.professions_reader.pagination import CloudReadOnlyPagination


class CloudReadOnlyModelViewSet(DynamicQuerysetMixin, ReadOnlyModelViewSet):
    """
    Base viewset for read-only endpoints using the 'cloud_readonly' DB.
    Supports search, filtering, ordering, field selection, pagination, and caching.
    """

    base_only_fields = []
    search_fields = []
    filterset_fields = []
    ordering_fields = []
    related_select_fields = []
    related_prefetch_fields = []
    pagination_class = CloudReadOnlyPagination
    cache_timeout = 60

    def get_queryset(self):
        cache_key = self._caching()
        cached_data = None
        try:
            cached_data = [
                obj.object for obj in deserialize("json", cache.get(cache_key))
            ]
        except Exception:  # noqa: BLE001
            cached_data = None  # noqa: F841
        return super().get_queryset()

    def _caching(self):
        user_part = ""
        if self.request.user.is_authenticated:
            user = self.request.user
            if hasattr(user, "project"):
                user_part = f"user_{user.project.uuid!s}"
            else:
                user_part = f"user_{user.pk!s}"
        time_part = (
            int(time.time() / 10) if not self.request.user.is_authenticated else 0
        )
        return f"{self.__class__.__name__}_{user_part}_{self.request.get_full_path()}_{time_part}"  # noqa: E501
