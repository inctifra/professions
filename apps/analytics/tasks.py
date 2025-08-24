# tasks.py
from http import HTTPStatus

from celery import shared_task
from django.apps import apps
from django.utils import timezone

from apps.analytics.api.serializers import APIUsageSummarySerializer
from apps.professions_reader.constants import MAX_INVALID_DOMAIN_REQUEST_COUNT
from apps.projects.models import Project

from .models import APIKey
from .models import APIRequestLog
from .models import APIUsageSummary


@shared_task
def log_api_request(data: dict) -> None:
    """
    ```json
    data should contain:
    {
        "api_key_id": int,
        "project_id": int,
        "endpoint": str,
        "method": str,
        "status_code": int,
        "response_time_ms": int,
        "ip_address": str,
        "user_agent": str,
        "error_message": str
    }
    ```
    """
    api_key = APIKey.objects.filter(key_id=data.get("api_key_id")).first()
    project = (
        Project.objects.filter(uuid=data.get("project_id")).first()
        if data.get("project_id")
        else None
    )

    # Log the request
    APIRequestLog.objects.create(
        project=project,
        api_key=api_key,
        endpoint=data.get("endpoint"),
        method=data.get("method", "GET"),
        status_code=data.get("status_code"),
        response_time_ms=data.get("response_time_ms", 0),
        ip_address=data.get("ip_address", ""),
        user_agent=data.get("user_agent", ""),
        error_message=data.get("error_message", ""),
    )

    # Update last_used_at
    if api_key:
        api_key.last_used_at = timezone.now()
        api_key.save(update_fields=["last_used_at"])

    # Update summary
    if api_key:
        today = timezone.now().date()
        summary, _ = APIUsageSummary.objects.get_or_create(api_key=api_key, date=today)
        summary.total_requests += 1
        if HTTPStatus.OK <= data.get("status_code", 0) < HTTPStatus.BAD_REQUEST:
            summary.success_requests += 1
        else:
            summary.error_requests += 1
        summary.avg_latency_ms = (
            summary.avg_latency_ms * (summary.total_requests - 1)
            + data.get("response_time_ms", 0)
        ) / summary.total_requests
        instance = summary.save()
        return APIUsageSummarySerializer(instance=instance).data
    return {}


@shared_task
def revoke_and_update_api_key_attempts(api_key_id):
    APIKey = apps.get_model("api_keys", "APIKey")
    api_key = APIKey.objects.get(key_id=api_key_id)
    api_key.failed_domain_attempts += 1
    update_fields = ["failed_domain_attempts"]

    # Only revoke if threshold crossed by this request
    if api_key.failed_domain_attempts >= MAX_INVALID_DOMAIN_REQUEST_COUNT:
        api_key.blacklisted = True
        api_key.status = "revoked"
        api_key.save()

    api_key.save(update_fields=update_fields)
    api_key.refresh_from_db()
    return str(api_key.uuid)


@shared_task
def unrevoke_and_update_api_key_attempts(api_key_id):
    APIKey = apps.get_model("api_keys", "APIKey")
    api_key = APIKey.objects.get(key_id=api_key_id)
    api_key.failed_domain_attempts = 0
    api_key.blacklisted = False
    api_key.status = "active"
    api_key.save()
    return str(api_key.uuid)
