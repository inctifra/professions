from rest_framework import serializers

from .models import Pharmacy
from .models import Pharmtech


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = "__all__"


class PharmtechSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmtech
        fields = "__all__"
