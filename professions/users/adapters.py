from __future__ import annotations

import typing

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.conf import settings

from professions.users.tasks import update_user_socialapp_avatar

if typing.TYPE_CHECKING:
    from allauth.socialaccount.models import SocialLogin
    from django.http import HttpRequest

from professions.users.models import User


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
    ) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def populate_user(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
        data: dict[str, typing.Any],
    ) -> User:
        """
        Populates user information from social provider info.

        See: https://docs.allauth.org/en/latest/socialaccount/advanced.html#creating-and-populating-user-instances
        """
        user = super().populate_user(request, sociallogin, data)
        if not user.name:
            if name := data.get("name"):
                user.name = name
            elif first_name := data.get("first_name"):
                user.name = first_name
                if last_name := data.get("last_name"):
                    user.name += f" {last_name}"
        if not user.avatar:
            provider = sociallogin.account.provider
            extra_data = sociallogin.account.extra_data
            avatar_url = None
            match provider:
                case "google":
                    avatar_url = extra_data.get("picture")
                case "github":
                    avatar_url = extra_data.get("avatar_url")
            if avatar_url:
                user.avatar = avatar_url
        return user

    def pre_social_login(self, request, sociallogin):
        """
        Merge accounts if the email exists with another provider.
        """

        email = sociallogin.user.email
        if not email:
            return

        try:
            existing_user = User.objects.get(email=email)

            # Check if this social provider is already linked
            provider = sociallogin.account.provider
            if not SocialAccount.objects.filter(
                user=existing_user, provider=provider
            ).exists():
                # Attach the new social account to the existing user
                sociallogin.connect(request, existing_user)

            # Update avatar if not set
            if not existing_user.avatar:
                extra_data = sociallogin.account.extra_data
                avatar_url = None
                match provider:
                    case "google":
                        avatar_url = extra_data.get("picture")
                    case "github":
                        avatar_url = extra_data.get("avatar_url")
                if avatar_url:
                    update_user_socialapp_avatar.delay(existing_user.pk, avatar_url)

        except User.DoesNotExist:
            # Let allauth create a new user
            pass
