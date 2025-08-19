from django.db import models

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
    url = models.URLField(max_length=200, default="https://docs.pkenya.makelaw.ke")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        if not self.pk and DeveloperDocumentation.objects.exists():
            DeveloperDocumentation.objects.all().delete()
        super().save(*args, **kwargs)
