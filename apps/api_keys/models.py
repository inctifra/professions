import secrets
import uuid

from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.db import models
from django.forms import ValidationError


class APIKey(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("revoked", "Revoked"),
    ]
    ACCESS_TYPE_CHOICES = [
        ("domain", "Domain"),
        ("project", "Project"),
    ]
    uuid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4, db_index=True,
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.PROTECT,
        related_name="api_keys",
        blank=True,
        null=True,
    )
    domain = models.ForeignKey(
        "projects.Domain",
        on_delete=models.PROTECT,
        related_name="api_keys",
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=100)
    key_id = models.CharField(max_length=32, unique=True, db_index=True, editable=False)
    secret_hash = models.CharField(max_length=128, editable=False)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="active", db_index=True,
    )
    permissions = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(blank=True, null=True)
    access_type = models.CharField(
        max_length=10, choices=ACCESS_TYPE_CHOICES, db_index=True,
    )
    failed_domain_attempts = models.PositiveIntegerField(default=0)
    blacklisted = models.BooleanField(default=False)
    _raw_key = None  # Private attribute to hold raw key temporarily

    def __str__(self):
        if getattr(self, "domain", None):
            return f"{self.name} ({self.domain.name})"
        if getattr(self, "project", None):
            return f"{self.name} ({self.project.name})"
        return self.name

    def save(self, *args, **kwargs):
        creating = self._state.adding  # True if it's a new object, before save
        if creating:
            raw_secret = secrets.token_urlsafe(32)
            self.key_id = secrets.token_hex(16)
            self.secret_hash = make_password(raw_secret)
            self._raw_key = f"{self.key_id}.{raw_secret}"
            print(self._raw_key)

        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        if self.project and self.domain:
            msg = "APIKey can be linked to either a project or a domain, not both."
            raise ValidationError(msg)
        if not self.project and not self.domain:
            msg = "APIKey must be linked to either a project or a domain."
            raise ValidationError(msg)

    def verify_secret(self, raw_secret):
        return check_password(raw_secret, self.secret_hash)

    @property
    def raw_key(self):
        """
        Returns the raw key once after creation; None afterwards.
        """
        return self._raw_key

    def regenerate_secret(self):
        """
        Optional: Regenerate secret for the key (admin-triggered).
        """
        raw_secret = secrets.token_urlsafe(32)
        self.secret_hash = make_password(raw_secret)
        self._raw_key = f"{self.key_id}.{raw_secret}"
        self.save()
        return self._raw_key


class APIKeySnapshot(models.Model):
    user = models.ForeignKey(
        "users.Profile",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="profile_keys_snapshots",
    )
    uuid = models.UUIDField(
        editable=False, unique=True, primary_key=True, db_index=True,
    )
    key = models.CharField(max_length=255, db_index=True)
    snapshot_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.uuid)
