from rest_framework import serializers

from .models import Pharmacy
from .models import Pharmtech, Accountant


class AccountantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accountant
        fields = "__all__"

class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = "__all__"


class PharmtechSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmtech
        fields = "__all__"
