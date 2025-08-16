from django.db.models import Count
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

from professions.analytics.models import APIRequestLog, APIUsageSummary


def get_api_usage_summary_chart_data(user):
    last_30_days = timezone.now().date() - timedelta(days=30)
    usage = (
        APIUsageSummary.objects.filter(
            api_key__project__user=user.profile, date__gte=last_30_days
        )
        .values("date")
        .annotate(
            total_requests=Sum("total_requests"),
            success_requests=Sum("success_requests"),
            error_requests=Sum("error_requests"),
        )
        .order_by("date")
    )

    return {
        "dates": [u["date"].strftime("%Y-%m-%d") for u in usage],
        "total": [u["total_requests"] for u in usage],
        "success": [u["success_requests"] for u in usage],
        "errors": [u["error_requests"] for u in usage],
    }


def get_top_endpoints_chart_data(user):
    logs = (
        APIRequestLog.objects.filter(project__user=user.profile)
        .values("endpoint")
        .annotate(total_requests=Count("id"))
        .order_by("-total_requests")[:10]
    )
    return {
        "endpoints": [log["endpoint"] for log in logs],
        "counts": [log["total_requests"] for log in logs],
    }
