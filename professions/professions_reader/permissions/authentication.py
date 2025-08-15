from urllib.parse import urlparse
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from professions.api_keys.models import APIKey


class APIKeyUser:
    """
    Minimal user-like object representing an API key context.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.project = api_key.project or getattr(api_key.domain, "project", None)
        self.domain = api_key.domain
        self.is_authenticated = True

    def __str__(self):
        return f"APIKeyUser(project={self.project}, domain={self.domain})"


class APIKeyAuthentication(BaseAuthentication):
    keyword = "PK-Api-Key"

    def authenticate(self, request):
        key_header = request.headers.get(self.keyword)
        if not key_header:
            return None

        try:
            key_id, raw_secret = key_header.split(".")
        except ValueError:
            msg = "Invalid API key format"
            raise AuthenticationFailed(msg) from msg

        try:
            api_key = APIKey.objects.get(key_id=key_id)
        except APIKey.DoesNotExist:
            msg = "Invalid API key"
            raise AuthenticationFailed(msg) from msg

        if api_key.status == "revoked":
            msg = "Your key has been revoked due to suspicious activities"
            raise AuthenticationFailed(msg)

        if not api_key.verify_secret(raw_secret):
            msg = "Invalid API key secret"
            raise AuthenticationFailed(msg)

        # --- DOMAIN VALIDATION ---
        request_domain = urlparse(request.build_absolute_uri()).netloc
        print("Request domain:", request_domain)

        allowed_domains = []
        if api_key.domain:
            allowed_domains = [urlparse(api_key.domain.url).netloc]
            print("Allowed domains:", allowed_domains)
        elif api_key.project:
            allowed_domains = [
                urlparse(url).netloc
                for url in api_key.project.domains.values_list("url", flat=True)
            ]
        request.domain_name = request_domain
        if request_domain not in allowed_domains:
            request.invalid_domain_attempt = True
            request.invalid_domain_name = request_domain
        return (APIKeyUser(api_key), None)
