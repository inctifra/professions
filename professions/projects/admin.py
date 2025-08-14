from django.contrib import admin

from .models import Domain
from .models import Project


class DomainInline(admin.TabularInline):
    model = Domain
    extra = 1
    fields = ("name", "is_verified", "created_at")
    readonly_fields = ("created_at",)
    show_change_link = True


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "plan", "is_active", "is_paid", "created_at")
    list_filter = ("is_active", "plan", "created_at", "is_paid")
    search_fields = ("name", "user__email", "plan__name")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    inlines = [DomainInline]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": ("name", "description", "user", "plan"),
                "classes": ("collapse",),
            },
        ),
        (
            "Status & Dates",
            {
                "fields": ("is_active", "is_paid", "created_at"),
                "classes": ("collapse",),
            },
        ),
    )
    readonly_fields = ("created_at", "is_paid")

    actions = ["activate_projects", "deactivate_projects"]

    @admin.action(description="Activate selected projects")
    def activate_projects(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Deactivate selected projects")
    def deactivate_projects(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "url", "is_verified", "created_at")
    list_filter = ("is_verified", "created_at", "project__plan")
    search_fields = ("name", "project__name", "project__user__email")
    ordering = ("name",)
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Domain Information",
            {
                "fields": ("name", "url", "project"),
                "classes": ("collapse",),
            },
        ),
        (
            "Verification & Dates",
            {
                "fields": ("is_verified", "created_at"),
                "classes": ("collapse",),
            },
        ),
    )
    readonly_fields = ("created_at",)

    actions = ["verify_domains", "unverify_domains"]

    @admin.action(description="Mark selected domains as verified")
    def verify_domains(self, request, queryset):
        queryset.update(is_verified=True)

    @admin.action(description="Mark selected domains as unverified")
    def unverify_domains(self, request, queryset):
        queryset.update(is_verified=False)
