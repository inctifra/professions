from django.contrib import admin

from .models import BillingRecord
from .models import Subscription


class BillingRecordInline(admin.TabularInline):
    model = BillingRecord
    extra = 0
    readonly_fields = ("created_at",)
    fields = (
        "amount",
        "currency",
        "status",
        "payment_method",
        "invoice_url",
        "created_at",
    )
    show_change_link = True


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "billing_cycle",
        "status",
        "is_active",
        "start_date",
        "end_date",
        "days_remaining",
    )
    list_filter = ("status", "is_active", "billing_cycle", "created_at")
    search_fields = ("project__name", "project__user__email")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    inlines = [BillingRecordInline]

    fieldsets = (
        (
            "Subscription Details",
            {
                "fields": ("project", "billing_cycle", "status", "is_active"),
                "classes": ("collapse",),
            },
        ),
        (
            "Dates",
            {
                "fields": ("start_date", "end_date"),
                "classes": ("collapse",),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )
    readonly_fields = ("start_date", "created_at")

    actions = ["activate_subscriptions", "deactivate_subscriptions"]

    @admin.action(description="Activate selected subscriptions")
    def activate_subscriptions(self, request, queryset):
        queryset.update(is_active=True, status="active")

    @admin.action(description="Deactivate selected subscriptions")
    def deactivate_subscriptions(self, request, queryset):
        queryset.update(is_active=False, status="canceled")


@admin.register(BillingRecord)
class BillingRecordAdmin(admin.ModelAdmin):
    list_display = (
        "subscription",
        "amount",
        "currency",
        "status",
        "payment_method",
        "created_at",
    )
    list_filter = ("status", "currency", "created_at")
    search_fields = ("subscription__project__name", "payment_method")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Billing Information",
            {
                "fields": (
                    "subscription",
                    "amount",
                    "currency",
                    "status",
                    "payment_method",
                    "invoice_url",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )
    readonly_fields = ("created_at",)

    actions = ["mark_as_paid", "mark_as_failed"]

    @admin.action(description="Mark selected billing records as paid")
    def mark_as_paid(self, request, queryset):
        queryset.update(status="paid")

    @admin.action(description="Mark selected billing records as failed")
    def mark_as_failed(self, request, queryset):
        queryset.update(status="failed")
