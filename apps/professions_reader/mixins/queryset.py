import json
import logging

from django.db.models import Q

logger = logging.getLogger(__file__)


class DynamicQuerysetMixin:
    """
    Handles dynamic search, filters, and ordering from query params.
    """

    def _dynamic_search(self, params, qs):
        search_raw = params.get("search")

        if search_raw and hasattr(self, "search_fields"):
            try:
                search_dict = json.loads(search_raw)
            except json.JSONDecodeError:
                return qs.none()  # invalid JSON = empty

            queries = Q()
            search_fields = search_dict.get("search_fields", {})

            has_non_empty_term = False
            for field, term in search_fields.items():
                if isinstance(term, str) and term.strip():
                    has_non_empty_term = True
                    queries |= Q(**{f"{field}__iexact": term.strip()})

            if has_non_empty_term:
                qs = qs.filter(queries)
            else:
                return qs.none()

        return qs

    def get_queryset(self):
        qs = super().get_queryset().using("cloud_readonly")
        params = self.request.query_params or self.request.data

        qs = self._dynamic_search(params, qs)

        if hasattr(self, "filterset_fields"):
            for field in self.filterset_fields:
                value = params.get(field)
                if value is not None:
                    qs = qs.filter(**{field: value})

        ordering = params.get("ordering")
        if ordering and hasattr(self, "ordering_fields"):
            if isinstance(ordering, str):
                ordering = ordering.split(",")
            allowed = [f.strip() for f in ordering if f.strip() in self.ordering_fields]
            if allowed:
                qs = qs.order_by(*allowed)

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
