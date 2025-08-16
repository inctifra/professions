import contextlib
from django.apps import AppConfig


class ApiKeysConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "professions.api_keys"

    def ready(self):
        with contextlib.suppress(ImportError):
            import professions.api_keys.signals  # noqa: F401, PLC0415
