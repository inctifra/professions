from django.contrib import admin

from .models import APIKey, APIKeySnapshot


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "project",
        "domain",
        "key_id",
        "status",
        "created_at",
        "last_used_at",
        "failed_domain_attempts",
        "blacklisted",
    )
    list_filter = ("status", "created_at", "project")
    search_fields = ("name", "key_id", "project__name")
    readonly_fields = (
        "key_id",
        "secret_hash",
        "created_at",
        "last_used_at",
        "display_raw_key",
        "failed_domain_attempts",
        "blacklisted",
    )
    ordering = ("-created_at",)
    fieldsets = (
        (None, {"fields": ("project", "domain", "name", "status", "permissions")}),
        (
            "Restrictions",
            {
                "fields": ("failed_domain_attempts", "blacklisted"),
                "classes": ("collapse",),
            },
        ),
        (
            "Keys",
            {
                "fields": ("key_id", "display_raw_key", "secret_hash"),
                "description": "Raw key is shown only once on creation.",
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "last_used_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def display_raw_key(self, obj):
        if obj and obj.raw_key:
            return f"<pre>{obj.raw_key}</pre>"
        return "—"

    display_raw_key.allow_tags = True
    display_raw_key.short_description = "Raw Key (One-time view)"

    actions = ["revoke_keys", "activate_keys"]

    @admin.action(description="Revoke selected API keys")
    def revoke_keys(self, request, queryset):
        updated = queryset.update(
            status="revoked", blacklisted=False, failed_domain_attempts=5
        )
        self.message_user(request, f"{updated} key(s) revoked.")

    @admin.action(description="Activate selected API keys")
    def activate_keys(self, request, queryset):
        updated = queryset.update(
            status="active", failed_domain_attempts=0, blacklisted=False
        )
        self.message_user(request, f"{updated} key(s) activated.")


@admin.register(APIKeySnapshot)
class APIKeySnapshotAdmin(admin.ModelAdmin):
    list_display = ("uuid", "key", "user", "snapshot_created_at")
    list_filter = ("user", "snapshot_created_at")
    search_fields = ("key", "uuid", "user__name")
    ordering = ("-snapshot_created_at",)
