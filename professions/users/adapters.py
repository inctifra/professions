from __future__ import annotations

import typing

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings

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
        user = super().populate_user(request, sociallogin, data)
        self._set_user_name(user, data)
        self._set_user_avatar(user, sociallogin)
        return user

    def _set_user_name(self, user: User, data: dict[str, typing.Any]) -> None:
        if user.name:
            return
        if name := data.get("name"):
            user.name = name
        elif first_name := data.get("first_name"):
            user.name = first_name
            if last_name := data.get("last_name"):
                user.name += f" {last_name}"

    def _set_user_avatar(self, user: User, sociallogin: SocialLogin) -> None:
        if user.avatar:
            return
        provider = sociallogin.account.provider
        extra_data = sociallogin.account.extra_data
        avatar_url = None

        match provider:
            case "google":
                avatar_url = extra_data.get("picture")
            case "facebook":
                avatar_url = f"https://graph.facebook.com/{extra_data.get('id')}/picture?type=large"
            case "github":
                avatar_url = extra_data.get("avatar_url")
            case "twitter":
                avatar_url = extra_data.get("profile_image_url_https")
        if avatar_url:
            user.avatar = avatar_url
