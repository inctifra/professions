from django.db import models
from django.core.exceptions import ValidationError

from apps.core.tasks import send_maintenance_notifications
# Create your models here.


class Contact(models.Model):
    title = models.CharField(
        max_length=10,
        choices=(("PHONE", "Phone"), ("EMAIL", "Email"), ("ADDRESS", "Address")),
        default="Phone",
        unique=True,
    )
    content = models.TextField()
    label = models.CharField(blank=True, max_length=300)
    icon = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.title


class DeveloperDocumentation(models.Model):
    url = models.URLField(
        max_length=200,
        default="https://docs.pkenya.co.ke",
        help_text="Mintlify Documentation",
        unique=True,
    )
    professional_endpoint = models.URLField(
        max_length=200,
        default="https://api.pkenya.co.ke",
        help_text="The endpoint for the professional api (paid)",
        unique=True,
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        if not self.pk and DeveloperDocumentation.objects.exists():
            DeveloperDocumentation.objects.all().delete()
        super().save(*args, **kwargs)


class SiteConfig(models.Model):
    maintenance_mode = models.BooleanField(default=False)
    site_name = models.CharField(max_length=255, default="My Website")
    contact_email = models.EmailField(default="info@example.com")
    # add more fields as needed

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return "Site Configuration"

    def save(self, *args, **kwargs):
        """Ensure only one SiteConfig instance exists."""
        if not self.pk and SiteConfig.objects.exists():
            msg = "Only one SiteConfig instance is allowed."
            raise ValidationError(msg)
        is_update = self.pk is not None
        old_mode = None
        if is_update:
            old_mode = SiteConfig.objects.get(pk=self.pk).maintenance_mode
        super().save(*args, **kwargs)
        if old_mode is True and self.maintenance_mode is False:
            send_maintenance_notifications.delay()

    @classmethod
    def get_solo(cls):
        """Helper to fetch the single instance (creates if not exists)."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class MaintenanceSubscriber(models.Model):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    notified = models.BooleanField(default=False)
    date_notified = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Maintenance Subscriber"
        verbose_name_plural = "Maintenance Subscribers"
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email
