from django.contrib import admin

from .models import APIRequestLog
from .models import APIUsageSummary


@admin.register(APIRequestLog)
class APIRequestLogAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "api_key",
        "endpoint",
        "method",
        "status_code",
        "response_time_ms",
        "ip_address",
        "timestamp",
    )
    list_filter = ("method", "status_code", "project", "api_key", "timestamp")
    search_fields = (
        "endpoint",
        "user_agent",
        "ip_address",
        "project__name",
        "api_key__name",
    )
    readonly_fields = (
        "project",
        "api_key",
        "endpoint",
        "method",
        "status_code",
        "response_time_ms",
        "error_message",
        "user_agent",
        "ip_address",
        "timestamp",
    )
    ordering = ("-timestamp",)
    date_hierarchy = "timestamp"
    list_per_page = 10


@admin.register(APIUsageSummary)
class APIUsageSummaryAdmin(admin.ModelAdmin):
    list_display = (
        "api_key",
        "date",
        "total_requests",
        "success_requests",
        "error_requests",
        "avg_latency_ms",
    )
    list_filter = ("api_key", "date")
    search_fields = ("api_key__name",)
    readonly_fields = (
        "api_key",
        "date",
        "total_requests",
        "success_requests",
        "error_requests",
        "avg_latency_ms",
    )
    ordering = ("-date",)
