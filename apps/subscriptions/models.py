from datetime import timedelta

from django.db import models
from django.utils import timezone

from apps.projects.models import Project


class Subscription(models.Model):
    BILLING_CHOICES = (
        ("monthly", "Monthly"),
        ("annually", "Annually"),
    )
    STATUS_CHOICES = [
        ("active", "Active"),
        ("canceled", "Canceled"),
        ("past_due", "Past Due"),
    ]

    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name="subscription",
    )
    billing_cycle = models.CharField(max_length=10, choices=BILLING_CHOICES, blank=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="active", db_index=True
    )
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        plan_name = (
            self.project.plan.get_name_display() if self.project.plan else "No plan"
        )
        return f"{self.project.name} - {plan_name}"

    def save(self, *args, **kwargs):
        # Set end_date only on creation
        if (
            self._state.adding
            and self.project.plan
            and self.project.is_paid
            and not self.end_date
        ):
            if self.billing_cycle == "monthly":
                self.end_date = self.start_date + timedelta(days=30)
            elif self.billing_cycle == "annually":
                self.end_date = self.start_date + timedelta(days=365)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        if self.project.plan and not self.project.plan.is_paid:
            return False
        return bool(self.end_date and timezone.now().date() > self.end_date)

    @property
    def days_remaining(self):
        return (
            max(0, (self.end_date - timezone.now().date()).days)
            if self.end_date
            else None
        )

    def renew(self, cycle=None):
        if cycle:
            self.billing_cycle = cycle
        self.start_date = timezone.now().date()
        if self.billing_cycle == "monthly":
            self.end_date = self.start_date + timezone.timedelta(days=30)
        elif self.billing_cycle == "annually":
            self.end_date = self.start_date + timezone.timedelta(days=365)

        self.status = "active"
        self.is_active = True
        self.save()


class BillingRecord(models.Model):
    STATUS_CHOICES = [
        ("paid", "Paid"),
        ("pending", "Pending"),
        ("failed", "Failed"),
    ]

    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, related_name="billing_records"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="KES")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending", db_index=True
    )
    payment_method = models.CharField(max_length=50)
    invoice_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Billing Record"
        verbose_name_plural = "Billing Records"

    def __str__(self):
        return f"Invoice {self.id} - {self.subscription.project.name} ({self.status})"
