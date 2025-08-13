import uuid

from django.db import models


class Project(models.Model):
    uuid = models.UUIDField(
        primary_key=True, editable=False, db_index=True, default=uuid.uuid4
    )
    user = models.ForeignKey(
        "users.Profile", on_delete=models.CASCADE, related_name="projects"
    )
    plan = models.ForeignKey(
        "plans.Plan", on_delete=models.PROTECT, related_name="projects"
    )
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return f"{self.name} ({self.user.email})"


class Domain(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="domains"
    )
    name = models.CharField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Domain"
        verbose_name_plural = "Domains"

    def __str__(self):
        return self.name
