from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from professions.plans.models import Feature, Plan

@login_required
def plans_view(request):
    plans = Plan.objects.prefetch_related("plan_features__feature").all()
    features = Feature.objects.all()

    context = {
        "plans": plans,
        "features": features
    }
    return render(request, "dashboard/pages/plans.html", context)
