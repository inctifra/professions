from decimal import Decimal
from django.core.management.base import BaseCommand
from apps.plans.models import Plan, Feature, PlanFeature

class Command(BaseCommand):
    help = "Seed the database with sample plans, features, and plan features"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding Features...")
        features_data = [
            {"name": "Basic Verification", "description": "Access to basic professional verification", "default_quota": 50},
            {"name": "Full Verification", "description": "Full verification with detailed report", "default_quota": 20},
            {"name": "Email Alerts", "description": "Receive email notifications on verification", "default_quota": 100},
            {"name": "API Access", "description": "Access to API endpoints", "default_quota": 1000},
            {"name": "Premium Support", "description": "Priority email and chat support", "default_quota": 0},
        ]

        features = []
        for fdata in features_data:
            feature, created = Feature.objects.get_or_create(name=fdata["name"], defaults=fdata)
            features.append(feature)
            if created:
                self.stdout.write(f"Created Feature: {feature.name}")

        self.stdout.write("Seeding Plans...")
        plans_data = [
            {"name": "B", "price": Decimal("150.00"), "request_limit": 100, "concurrency_limit": 1, "description": "Basic plan for small projects"},
            {"name": "S", "price": Decimal("500.00"), "request_limit": 500, "concurrency_limit": 2, "description": "Standard plan for growing teams"},
            {"name": "P", "price": Decimal("1000.00"), "request_limit": 2000, "concurrency_limit": 5, "description": "Premium plan for enterprises"},
        ]

        plans = {}
        for pdata in plans_data:
            plan, created = Plan.objects.get_or_create(name=pdata["name"], defaults=pdata)
            plans[pdata["name"]] = plan
            if created:
                self.stdout.write(f"Created Plan: {plan}")

        self.stdout.write("Assigning Plan Features...")
        plan_features_map = {
            "B": {
                "Basic Verification": 50,
                "API Access": 1000,
            },
            "S": {
                "Basic Verification": 100,
                "Full Verification": 20,
                "API Access": 3000,
                "Email Alerts": 50,
            },
            "P": {
                "Basic Verification": 200,
                "Full Verification": 50,
                "API Access": 10000,
                "Email Alerts": 200,
                "Premium Support": None,
            },
        }

        for plan_name, feature_limits in plan_features_map.items():
            plan = plans[plan_name]
            for fname, limit in feature_limits.items():
                feature = Feature.objects.get(name=fname)
                pf, created = PlanFeature.objects.get_or_create(plan=plan, feature=feature, defaults={"limit": limit})
                if created:
                    self.stdout.write(f"Assigned Feature '{feature.name}' to Plan '{plan.get_name_display()}' with limit {limit or 'Unlimited'}")

        self.stdout.write(self.style.SUCCESS("Seeding completed!"))
