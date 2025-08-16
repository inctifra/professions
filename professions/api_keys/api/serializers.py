from rest_framework import serializers

from professions.api_keys.models import APIKey


class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = [
            "uuid",
            "name",
            "status",
            "permissions",
            "created_at",
            "last_used_at",
            "access_type",
        ]
