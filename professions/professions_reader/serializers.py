from rest_framework import serializers

from .models import Accountant
from .models import Advocate
from .models import Pharmacy
from .models import Pharmtech

# NOTE: A lot of imports are dynamic therefore there is strict naming convention

"""
For example: import of serializer class is dynamic based on the
name of the model which is also selected dynamically

modelNameSerializer
---------------------------
any defiant will lead to breakage of the application


For issues contact Developer:<email: inctifra@gmail.com>

"""


class AccountantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accountant
        fields = "__all__"


class AdvocateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advocate
        fields = "__all__"


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = "__all__"


class PharmtechSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmtech
        fields = "__all__"
