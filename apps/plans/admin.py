from django.contrib import admin

from .models import Feature
from .models import Plan
from .models import PlanFeature


class PlanFeatureInline(admin.TabularInline):
    model = PlanFeature
    extra = 1
    autocomplete_fields = ("feature",)


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        "get_name_display",
        "price",
        "request_limit",
        "concurrency_limit",
        "created_at",
    )
    list_filter = ("name",)
    search_fields = ("name", "description")
    ordering = ("name",)
    inlines = [PlanFeatureInline]

    fieldsets = (
        (
            "Plan Information",
            {
                "fields": ("name", "description"),
                "description": "Select the plan type and provide a brief description.",
            },
        ),
        (
            "Pricing & Limits",
            {
                "fields": ("price", "request_limit", "concurrency_limit"),
                "description": "You can override the default KES price if needed.",
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at",),
            },
        ),
    )

    readonly_fields = ("created_at",)

    def save_model(self, request, obj, form, change):
        """Set default prices based on plan type if price is not manually changed."""
        default_prices = {"B": 50, "S": 250, "P": 500}
        if not change and obj.name in default_prices and obj.price in [None, 0]:
            obj.price = default_prices[obj.name]
        super().save_model(request, obj, form, change)


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("name", "default_quota")
    search_fields = ("name", "description")
    fieldsets = (
        (
            "Feature Details",
            {
                "fields": ("name", "description"),
            },
        ),
        (
            "Default Quota",
            {
                "fields": ("default_quota",),
            },
        ),
    )


@admin.register(PlanFeature)
class PlanFeatureAdmin(admin.ModelAdmin):
    list_display = ("plan", "feature", "limit")
    list_filter = ("plan", "feature")
    search_fields = ("plan__name", "feature__name")
    fieldsets = (
        (
            "Plan Feature Mapping",
            {
                "fields": ("plan", "feature"),
            },
        ),
        (
            "Limit Settings",
            {
                "fields": ("limit",),
            },
        ),
    )
