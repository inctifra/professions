from django.db import connection
from storages.backends.s3boto3 import S3Boto3Storage


class TenantMediaStorage(S3Boto3Storage):
    location = "media"

    def _add_schema_prefix(self, name):
        try:
            schema = getattr(connection, "tenant", None)
            schema_name = getattr(schema, "schema_name", "public")
        except (Exception, ValueError):
            return f"public/{name}"
        return f"{schema_name}/{name}"

    def _normalize_name(self, name):
        name = self._add_schema_prefix(name)
        return super()._normalize_name(name)

    def get_available_name(self, name, max_length=None):
        name = self._add_schema_prefix(name)
        return super().get_available_name(name, max_length)
