from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from professions.api_keys.models import APIKeySnapshot

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import Profile, User

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://docs.allauth.org/en/latest/common/admin.html#admin
    admin.autodiscover()
    admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]


class APIKeySnapshotInline(admin.TabularInline):
    model = APIKeySnapshot
    fields = ("uuid", "key", "snapshot_created_at")
    readonly_fields = ("uuid", "key", "snapshot_created_at")
    extra = 0


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name", "avatar")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "name", "is_superuser"]
    search_fields = ["name"]
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [APIKeySnapshotInline]
    list_display = (
        "get_user_email",
        "bio_summary",
        "avatar_thumbnail",
        "is_active_user",
    )
    list_filter = ("user__is_active",)
    search_fields = ("user__email", "bio")
    list_display_links = ("get_user_email",)
    readonly_fields = ("avatar_thumbnail",)

    def get_user_email(self, obj):
        return obj.user.email

    get_user_email.short_description = "Email"

    def bio_summary(self, obj):
        if obj.bio:
            return obj.bio[:50] + "..." if len(obj.bio) > int("50") else obj.bio
        return "-"

    bio_summary.short_description = "Bio"

    def avatar_thumbnail(self, obj):
        if obj.avatar:
            return f"""
        <img src="{obj.avatar.url}" width="50" height="50" style="border-radius:50%;" />
        """
        return "-"

    avatar_thumbnail.allow_tags = True
    avatar_thumbnail.short_description = "Avatar"

    def is_active_user(self, obj):
        return obj.user.is_active

    is_active_user.boolean = True
    is_active_user.short_description = "Active?"
