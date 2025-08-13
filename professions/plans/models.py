from decimal import Decimal

from django.db import models


class Plan(models.Model):
    PLAN_CHOICES = (
        ("B", "Basic"),
        ("S", "Standard"),
        ("P", "Premium"),
    )

    DEFAULT_PRICES = {
        "B": Decimal("50.00"),
        "S": Decimal("250.00"),
        "P": Decimal("500.00"),
    }
    name = models.CharField(
        max_length=1,
        choices=PLAN_CHOICES,
        unique=True,
        default="B",
        help_text="Plan type: Basic, Standard, or Premium",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Monthly price in KES",
    )
    request_limit = models.PositiveIntegerField(
        help_text="Requests allowed per month", default=100
    )
    concurrency_limit = models.PositiveIntegerField(
        default=1, help_text="Max concurrent requests"
    )
    description = models.TextField(blank=True)
    is_paid = models.BooleanField(default=True, help_text="Whether this is a paid plan")
    created_at = models.DateTimeField(auto_now_add=True)

    # Features
    features = models.ManyToManyField(
        "Feature", through="PlanFeature", related_name="plans"
    )

    # Optional throttling limits
    requests_per_second = models.PositiveIntegerField(
        null=True, blank=True, help_text="Maximum requests per second for this plan."
    )
    requests_per_minute = models.PositiveIntegerField(
        null=True, blank=True, help_text="Maximum requests per minute for this plan."
    )

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"
        ordering = ["name"]

    def __str__(self):
        return f"{self.get_name_display()} - {self.price or 'Free'} KES"

    def save(self, *args, **kwargs):
        # Auto-assign default price only if creating and price not provided
        if self._state.adding and self.price is None:
            self.price = self.DEFAULT_PRICES.get(self.name, Decimal("0.00"))
        super().save(*args, **kwargs)


class Feature(models.Model):
    """Feature that can be attached to plans."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    default_quota = models.PositiveIntegerField(
        default=0, help_text="Default quota for this feature"
    )

    class Meta:
        verbose_name = "Feature"
        verbose_name_plural = "Features"
        ordering = ["name"]

    def __str__(self):
        return self.name


class PlanFeature(models.Model):
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, related_name="plan_features"
    )
    feature = models.ForeignKey(
        Feature, on_delete=models.CASCADE, related_name="feature_plans"
    )
    limit = models.PositiveIntegerField(
        null=True, blank=True, help_text="Custom limit for this feature under this plan"
    )

    class Meta:
        unique_together = ("plan", "feature")
        verbose_name = "Plan Feature"
        verbose_name_plural = "Plan Features"
        ordering = ["plan__name", "feature__name"]

    def __str__(self):
        return f"""{self.plan.get_name_display()} -
    {self.feature.name} ({self.limit or "Unlimited"})"""
