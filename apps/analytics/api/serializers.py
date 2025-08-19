from rest_framework import serializers

from apps.analytics.models import APIRequestLog
from apps.analytics.models import APIUsageSummary
from apps.api_keys.api.serializers import APIKeySerializer


class APIRequestLogSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.name", read_only=True)

    class Meta:
        model = APIRequestLog
        fields = [
            "id",
            "project",
            "project_name",
            "api_key",
            "api_key_name",
            "endpoint",
            "method",
            "status_code",
            "response_time_ms",
            "error_message",
            "user_agent",
            "ip_address",
            "timestamp",
        ]
        read_only_fields = ["timestamp"]


class APIUsageSummarySerializer(serializers.ModelSerializer):
    api_key_name = serializers.CharField(source="api_key.name", read_only=True)
    api_key = APIKeySerializer(read_only=True)

    class Meta:
        model = APIUsageSummary
        fields = [
            "id",
            "api_key",
            "api_key_name",
            "date",
            "total_requests",
            "success_requests",
            "error_requests",
            "avg_latency_ms",
        ]
        read_only_fields = [
            "total_requests",
            "success_requests",
            "error_requests",
            "avg_latency_ms",
        ]
