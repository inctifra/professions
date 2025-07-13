from rest_framework import serializers

from professions.core.models import Contact


class ContactModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class ProfessionalLookupSerializer(serializers.Serializer):
    model_name = serializers.CharField(max_length=300)
    professional_name = serializers.CharField(max_length=100)
