from django.db import models


class Feature(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.SlugField(unique=True)  # e.g. 'api_keys', 'projects'
    description = models.TextField(blank=True)
    default_limit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Plan(models.Model):
    PLAN_CHOICES = [
        ("free", "Free"),
        ("basic", "Basic"),
        ("business", "Business"),
    ]
    name = models.CharField(
        max_length=50, choices=PLAN_CHOICES, default="free", unique=True
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    features = models.ManyToManyField(Feature, through="PlanFeature")
    is_paid = models.BooleanField(default=False)
    price_monthly = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    price_annually = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_paid and self.price_monthly:
            annual_price = self.price_monthly * 12
            discount = annual_price * 0.20
            self.price_annually = annual_price - discount
        else:
            self.price_annually = None
        super().save(*args, **kwargs)


class PlanFeature(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    limit = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("plan", "feature")

    def __str__(self):
        return f"{self.plan.name} - {self.feature.name} ({self.limit})"
