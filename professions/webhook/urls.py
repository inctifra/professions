from django.urls import path

from .views import stripe_webhook
app_name = "webhooks"
urlpatterns = [
    path("stripe/", stripe_webhook, name="stripe"),
]
