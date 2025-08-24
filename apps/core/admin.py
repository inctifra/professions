from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from apps.core.tasks import send_maintenance_notifications

from .models import Contact
from .models import MaintenanceSubscriber
from .models import SiteConfig


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["title", "label", "icon", "content"]


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    # Fields to display in the admin list page
    list_display = ("site_name", "contact_email", "maintenance_mode")

    # Fields searchable in admin
    search_fields = ("site_name", "contact_email")

    # Filters in the right sidebar
    list_filter = ("maintenance_mode",)

    # Fields grouped in the detail page
    fieldsets = (
        ("General Settings", {"fields": ("site_name", "contact_email")}),
        (
            "Maintenance",
            {
                "fields": ("maintenance_mode",),
                "description": (
                    """Enable maintenance mode to show the maintenance page to
                    non-staff users."""
                ),
            },
        ),
    )

    # Read-only fields (if you want some fields locked)
    readonly_fields = ()

    def has_add_permission(self, request):
        """Prevent adding more than one config instance."""
        return not SiteConfig.objects.exists()

    def changelist_view(self, request, extra_context=None):
        """Redirect list view to the single instance edit page."""
        config = SiteConfig.get_solo()
        return HttpResponseRedirect(
            reverse("admin:core_siteconfig_change", args=[config.pk])
        )


@admin.action(description="Mark selected subscribers as notified")
def mark_as_notified(modeladmin, request, queryset):
    queryset.update(notified=True, date_notified=timezone.now())

    # Trigger Celery task for sending emails
    # Pass the IDs of selected subscribers if you want selective sending
    # subscriber_ids = list(queryset.values_list("id", flat=True))  # noqa: ERA001
    send_maintenance_notifications.delay()


@admin.register(MaintenanceSubscriber)
class MaintenanceSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "date_joined", "notified", "date_notified")
    list_filter = ("notified", "date_joined")
    search_fields = ("email",)
    readonly_fields = ("date_joined", "date_notified")
    actions = [mark_as_notified]

    fieldsets = (
        (None, {"fields": ("email",)}),
        (
            "Status",
            {
                "fields": ("notified", "date_notified"),
                "description": """
                Shows whether the subscriber has been notified when maintenance ended.
                """,
            },
        ),
        ("Timestamps", {"fields": ("date_joined",)}),
    )

    def get_readonly_fields(self, request, obj=None):
        """Make notified/date_notified read-only if object exists"""
        ro_fields = list(self.readonly_fields)
        if obj:
            ro_fields.append("notified")  # optionally prevent manual toggle
        return ro_fields
