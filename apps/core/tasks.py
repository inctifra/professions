from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone


@shared_task
def send_maintenance_notifications():
    from .models import MaintenanceSubscriber  # noqa: PLC0415
    from .models import SiteConfig  # noqa: PLC0415

    subscribers = MaintenanceSubscriber.objects.filter(notified=False)
    site_email = SiteConfig.get_solo().contact_email

    for sub in subscribers:
        send_mail(
            subject="Website is Back Online!",
            message=f"Hello {sub.email}! Our site is now live. Check it out!",
            from_email=site_email,
            recipient_list=[sub.email],
            fail_silently=True,
        )
        sub.notified = True
        sub.date_notified = timezone.now()
        sub.save()
