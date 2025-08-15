from datetime import timedelta

from django.utils import timezone

from professions.projects.models import Project
from professions.subscriptions.models import BillingRecord
from professions.subscriptions.models import Subscription


def create_subscription_and_billing(
    project: Project,
    payment_method: str = "card",
    amount=None,
    billing_cycle: str = "monthly",
    invoice_url: str = "",
):
    """
    Create a subscription and a billing record for a project.
    """
    if not project.is_paid:
        project.is_paid = True
        project.is_active = True
        project.save()

    # Use project.plan.price if amount not provided
    if amount is None and project.plan:
        amount = project.plan.price

    subscription, created = Subscription.objects.get_or_create(
        project=project,
        defaults={
            "billing_cycle": billing_cycle,
            "start_date": timezone.now().date(),
            "status": "active",
        },
    )

    if created or not subscription.end_date:
        # Set end_date based on billing_cycle
        if subscription.billing_cycle == "monthly":
            subscription.end_date = subscription.start_date + timedelta(days=30)
        elif subscription.billing_cycle == "annually":
            subscription.end_date = subscription.start_date + timedelta(days=365)
        subscription.is_active = True
        subscription.status = "active"
        subscription.save()

    # Create billing record
    BillingRecord.objects.create(
        subscription=subscription,
        amount=amount,
        currency="KES",
        status="paid",
        payment_method=payment_method,
        invoice_url=invoice_url,
    )

    return subscription
