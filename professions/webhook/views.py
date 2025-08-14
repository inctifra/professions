# payments/webhooks.py
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from professions.projects.models import Project
from professions.subscriptions.models import BillingRecord
from professions.subscriptions.models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    # Only handle completed checkout sessions
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        project_uuid = session.get("client_reference_id")

        if project_uuid:
            project = Project.objects.filter(uuid=project_uuid).first()
            if project and not project.is_paid:
                # Mark project as paid & active
                project.is_paid = True
                project.is_active = True
                project.save()

                # Create Subscription if not exists
                subscription, created = Subscription.objects.get_or_create(
                    project=project,
                    defaults={
                        "billing_cycle": "monthly",  # default; later could be dynamic
                        "start_date": timezone.now().date(),
                        "status": "active",
                    },
                )

                if created:
                    # Set end_date based on billing_cycle
                    if subscription.billing_cycle == "monthly":
                        subscription.end_date = (
                            subscription.start_date + timezone.timedelta(days=30)
                        )
                    elif subscription.billing_cycle == "annually":
                        subscription.end_date = (
                            subscription.start_date + timezone.timedelta(days=365)
                        )
                    subscription.save()

                # Create initial Billing Record
                BillingRecord.objects.create(
                    subscription=subscription,
                    amount=project.plan.price,
                    currency="KES",
                    status="paid",
                    payment_method="card",  # could be fetched from session if needed
                    invoice_url=session.get("invoice", ""),  # optional
                )

    return HttpResponse(status=200)
