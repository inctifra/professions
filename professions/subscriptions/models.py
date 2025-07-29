from django.conf import settings
from django.db import models
from django.utils import timezone

from professions.plans.models import Feature
from professions.plans.models import Plan


class Subscription(models.Model):
    BILLING_CHOICES = (
        ("monthly", "Monthly"),
        ("annually", "Annually"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    billing_cycle = models.CharField(max_length=10, choices=BILLING_CHOICES, blank=True)

    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.plan}"

    def save(self, *args, **kwargs):
        if self.plan and self.plan.is_paid and not self.end_date:
            if self.billing_cycle == "monthly":
                self.end_date = self.start_date + timezone.timedelta(days=30)
            elif self.billing_cycle == "annually":
                self.end_date = self.start_date + timezone.timedelta(days=365)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        if self.plan and not self.plan.is_paid:
            return False
        return self.end_date and timezone.now().date() > self.end_date

    @property
    def days_remaining(self):
        if not self.end_date:
            return None
        return max(0, (self.end_date - timezone.now().date()).days)


class Domain(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    domain_name = models.CharField(max_length=255, unique=True, help_text="pkenya.com")
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.domain_name


class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.domain.domain_name})"


class FeatureUsage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    used = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "feature")

    def __str__(self):
        return f"{self.user} - {self.feature.name} (Used: {self.used})"
