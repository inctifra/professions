import time

from django.core.cache import cache
from django.core.serializers import deserialize
from django.core.serializers import serialize
from django.db.models import Q
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.professions_reader.pagination import CloudReadOnlyPagination


class CloudReadOnlyModelViewSet(ReadOnlyModelViewSet):
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
        cache_key = f"{self.__class__.__name__}_{user_part}_{self.request.get_full_path()}_{time_part}"
        cached_data = None
        try:
            cached_data = [
                obj.object for obj in deserialize("json", cache.get(cache_key))
            ]
        except Exception:  # noqa: BLE001
            cached_data = None

        if cached_data is not None:
            print("cached data: ", cached_data)
            return cached_data[0]

        # Build queryset
        qs = self.queryset.using("cloud_readonly").all()
        qs = self._apply_base_only_fields(qs)
        qs = self._optimize_related(qs)
        qs = self._apply_search(qs)
        qs = self._apply_filters(qs)
        qs = self._apply_ordering(qs)

        qs_list = qs

        cached_value = serialize("json", list(qs_list))
        cache.set(cache_key, cached_value, self.cache_timeout)

        return qs_list

    def _apply_base_only_fields(self, qs):
        if self.base_only_fields:
            return qs.only(*self.base_only_fields)
        return qs

    def _optimize_related(self, qs):
        if self.related_select_fields:
            qs = qs.select_related(*self.related_select_fields)
        if self.related_prefetch_fields:
            qs = qs.prefetch_related(*self.related_prefetch_fields)
        return qs

    def _apply_search(self, qs):
        search = self.request.query_params.get("search")
        if search and self.search_fields:
            queries = Q()
            for field in self.search_fields:
                queries |= Q(**{f"{field}__icontains": search})
            return qs.filter(queries)
        return qs

    def _apply_filters(self, qs):
        for field in self.filterset_fields:
            value = self.request.query_params.get(field)
            if value:
                qs = qs.filter(**{field: value})
        return qs

    def _apply_ordering(self, qs):
        ordering = self.request.query_params.get("ordering")
        if ordering and self.ordering_fields:
            allowed = [
                f.strip()
                for f in ordering.split(",")
                if f.strip() in self.ordering_fields
            ]
            if allowed:
                return qs.order_by(*allowed)
        if self.ordering_fields:
            return qs.order_by(*self.ordering_fields)
        return qs
