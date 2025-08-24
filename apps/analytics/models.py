from django.db import models

from apps.api_keys.models import APIKey
from apps.projects.models import Project


class APIRequestLog(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        related_name="api_logs",
        blank=True,
        null=True,
    )
    api_key = models.ForeignKey(
        APIKey,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="usage_logs",
    )
    endpoint = models.CharField(max_length=255, db_index=True)
    method = models.CharField(max_length=10, db_index=True)
    status_code = models.PositiveIntegerField(db_index=True)
    response_time_ms = models.PositiveIntegerField()
    error_message = models.TextField(blank=True)
    user_agent = models.CharField(max_length=512, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["timestamp"]),
            models.Index(fields=["project", "timestamp"]),
            models.Index(fields=["api_key", "timestamp"]),
        ]
        ordering = ["-timestamp"]

    def __str__(self):
        proj_name = self.project.name if self.project else "No Project"
        return f"{proj_name} - {self.endpoint} @ {self.timestamp}"


class APIUsageSummary(models.Model):
    api_key = models.ForeignKey(
        APIKey,
        on_delete=models.CASCADE,
        related_name="usage_summary",
    )
    date = models.DateField(db_index=True)
    total_requests = models.PositiveIntegerField(default=0)
    success_requests = models.PositiveIntegerField(default=0)
    error_requests = models.PositiveIntegerField(default=0)
    avg_latency_ms = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ("api_key", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.api_key.name} - {self.date}"
