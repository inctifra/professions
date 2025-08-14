from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("create", views.create_project_view, name="create"),
    path(
        "purchase/<uuid>/update",
        views.update_project_purchase_view,
        name="project_purchase_update",
    ),
    path("<uuid>/checkout", views.project_purchase_checkout, name="checkout"),
    path(
        "<uuid>/checkout/success",
        views.project_purchase_success_view,
        name="payment_success",
    ),
    path(
        "<uuid>/checkout/cancel",
        views.project_purchase_cancel_view,
        name="payment_cancel",
    ),
]
