from rest_framework import serializers

from apps.plans.models import Feature
from apps.plans.models import Plan
from apps.plans.models import PlanFeature


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ["id", "name", "code", "description", "default_limit"]


class PlanFeatureSerializer(serializers.ModelSerializer):
    feature = FeatureSerializer()

    class Meta:
        model = PlanFeature
        fields = ["id", "feature", "limit"]


class PlanSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = [
            "id",
            "name",
            "description",
            "is_active",
            "is_paid",
            "price_monthly",
            "price_annually",
            "features",
        ]

    def get_features(self, obj):
        plan_features = PlanFeature.objects.filter(plan=obj)
        return PlanFeatureSerializer(plan_features, many=True).data
