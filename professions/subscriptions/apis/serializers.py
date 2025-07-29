from rest_framework import serializers

from professions.plans.apis.serializers import FeatureSerializer
from professions.plans.apis.serializers import PlanSerializer
from professions.subscriptions.models import Domain
from professions.subscriptions.models import FeatureUsage
from professions.subscriptions.models import Project
from professions.subscriptions.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    is_expired = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()

    class Meta:
        model = Subscription
        fields = [
            "id",
            "user",
            "plan",
            "billing_cycle",
            "start_date",
            "end_date",
            "is_active",
            "is_expired",
            "days_remaining",
        ]


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ["id", "user", "domain_name", "verified", "created", "updated"]


class ProjectSerializer(serializers.ModelSerializer):
    domain = DomainSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ["id", "user", "domain", "name", "created"]


class FeatureUsageSerializer(serializers.ModelSerializer):
    feature = FeatureSerializer(read_only=True)

    class Meta:
        model = FeatureUsage
        fields = ["id", "user", "feature", "used", "updated"]


class WritableDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ["id", "user", "domain_name", "verified"]


class WritableProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "user", "domain", "name"]


class WritableFeatureUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureUsage
        fields = ["id", "user", "feature", "used"]
