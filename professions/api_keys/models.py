import secrets
import uuid

from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.db import models


class APIKey(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("revoked", "Revoked"),
    ]
    uuid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4, db_index=True
    )
    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="api_keys"
    )
    domain = models.ForeignKey(
        "projects.Domain", on_delete=models.CASCADE, related_name="api_keys"
    )
    name = models.CharField(max_length=100)
    key_id = models.CharField(max_length=32, unique=True, db_index=True, editable=False)
    secret_hash = models.CharField(max_length=128, editable=False)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="active", db_index=True
    )
    permissions = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(blank=True, null=True)

    _raw_key = None  # Private attribute to hold raw key temporarily

    def __str__(self):
        return f"{self.name} ({self.project.name})"

    def save(self, *args, **kwargs):
        if not self.pk:  # Only generate new keys when creating
            raw_secret = secrets.token_urlsafe(32)
            self.key_id = secrets.token_hex(16)
            self.secret_hash = make_password(raw_secret)
            self._raw_key = f"{self.key_id}.{raw_secret}"
            # Store raw key for one-time display
        super().save(*args, **kwargs)

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
