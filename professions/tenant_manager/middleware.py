from django.contrib.auth.middleware import LoginRequiredMiddleware as BaseLoginRequired
from django.db import connection


class SchemaAwareLoginRequiredMiddleware(BaseLoginRequired):
    def __call__(self, request):
        if (
            getattr(connection, "tenant", None)
            and connection.tenant.schema_name == "public"
        ):
            return self.get_response(request)
        return super().__call__(request)
