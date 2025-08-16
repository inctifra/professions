from django.db.models import Avg
from django.db.models import Count
from django.db.models import ExpressionWrapper
from django.db.models import F
from django.db.models import FloatField
from django.db.models import Q
from django.db.models import Value
from django.db.models.functions import Cast
from django.db.models.functions import Length
from django.db.models.functions import Reverse
from django.db.models.functions import StrIndex
from django.db.models.functions import Substr

from professions.analytics.models import APIRequestLog


def compose_analytics_context(request):
    if request.path.startswith("/api/"):
        return {}

    if request.user.is_authenticated:
        # filter all logs belonging to this user
        logs_qs = APIRequestLog.objects.filter(
            Q(project__user=request.user.profile)
            | Q(api_key__domain__project__user=request.user.profile)
            | Q(api_key__project__user=request.user.profile)
        )

        # get global total across ALL keys (for percentage denominator)
        total_requests_all = logs_qs.aggregate(total=Count("id"))["total"] or 1

        # group per api_key + resource
        logs = (
            logs_qs.annotate(
                endpoint_trimmed=Substr(F("endpoint"), 1, Length("endpoint") - 1),
                reversed_endpoint=Reverse(F("endpoint_trimmed")),
                slash_index=StrIndex(F("reversed_endpoint"), Value("/")),
                last_segment_reversed=Substr(
                    F("reversed_endpoint"), 1, F("slash_index") - 1
                ),
                resource=Reverse(F("last_segment_reversed")),
            )
            .values("api_key", "api_key__name", "endpoint", "resource")
            .annotate(
                total_requests=Count("id"),
                avg_response_time=Avg("response_time_ms"),
                percentage=ExpressionWrapper(
                    Cast(Count("id"), FloatField()) * 100.0 / float(total_requests_all),
                    output_field=FloatField(),
                ),
            )
            .order_by("api_key", "endpoint")
        )

        return {"api_logs": logs}

    return {}
