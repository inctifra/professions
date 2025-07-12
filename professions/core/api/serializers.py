from rest_framework import serializers

from professions.core.models import Contact


class ContactModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
