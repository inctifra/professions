from urllib.parse import urlparse

from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from apps.professions_reader.constants import MAX_INVALID_DOMAIN_REQUEST_COUNT


class HasValidAPIKey(BasePermission):
    """
    Allows access only if the request has a valid API key
    and the request comes from an allowed domain.
    """

    def has_permission(self, request, view):
        user = self.get_user(request)
        request_domain = request.domain_name
        if (
            hasattr(request, "allowed_domains")
            and request_domain in request.allowed_domains
        ):
            return True
        if not self.is_valid_domain(user, request_domain):
            raise self.handle_invalid_domain(user, request_domain)
        return True

    def get_user(self, request):
        user = getattr(request, "user", None)
        if not user:
            msg = "No API user associated with this request."
            raise PermissionDenied(msg)
        return user

    def get_api_key(self, user):
        api_key = getattr(user, "api_key", None)
        if not api_key:
            msg = "Invalid or missing API key."
            raise PermissionDenied(msg)
        return api_key

    def is_valid_domain(self, user, request_domain):
        if getattr(user, "domain", None):
            return urlparse(user.domain.url).netloc == request_domain
        if getattr(user, "project", None):
            allowed_domains = [
                urlparse(url).netloc
                for url in user.project.domains.values_list("url", flat=True)
            ]
            return request_domain in allowed_domains
        return False

    def handle_invalid_domain(self, user, request_domain):
        """
        Increment failed attempts asynchronously and blacklist if threshold exceeded.
        """
        attempts = int(
            MAX_INVALID_DOMAIN_REQUEST_COUNT - (user.api_key.failed_domain_attempts + 1)
        )
        if getattr(user, "domain", None):
            msg = (
                f"API key is only allowed from domain: {user.domain.name} =>({urlparse(user.domain.url).netloc}). "  # noqa: E501
                f"Your request came from: {request_domain}. "
                f"You have {attempts}"
                " attempts after which your key will be revoked permanently"
            )
        else:
            allowed_domains = [
                urlparse(url).netloc
                for url in user.project.domains.values_list("url", flat=True)
            ]
            msg = (
                f"API key is allowed from project domains: {', '.join(allowed_domains)}. "  # noqa: E501
                f"Your request came from: {request_domain}. "
                f"You have {attempts}"
                " attempts after which your key will be revoked permanently"
            )

        raise PermissionDenied(msg)
