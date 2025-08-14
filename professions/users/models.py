from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for professions.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    avatar = models.URLField(blank=True, max_length=2000)

    objects: ClassVar[UserManager] = UserManager()

    def save(self, *args, **kwargs):
        # If name is empty, set it to the part before '@' in the email
        if not self.name and self.email:
            self.name = self.email.split("@")[0]
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.
        Returns:
            str: URL for user detail.
        """
        return reverse("users:detail", kwargs={"pk": self.id})

    def get_display_name(self):
        """
        Return the user's name, or the first part of their email if no name is set.
        """
        return self.name or (self.email.split("@")[0] if self.email else "")

    def __str__(self):
        return self.get_display_name()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"
