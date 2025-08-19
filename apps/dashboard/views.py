import json
from datetime import timedelta

import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models import F
from django.db.models import Q
from django.db.models import Sum
from django.db.models import Value
from django.db.models.functions import Length
from django.db.models.functions import Reverse
from django.db.models.functions import StrIndex
from django.db.models.functions import Substr
from django.http import HttpRequest
from django.http import JsonResponse
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.base import TemplateView

from apps.analytics.models import APIRequestLog
from apps.analytics.models import APIUsageSummary
from apps.api_keys.forms import APIKeyForm
from apps.api_keys.models import APIKey
from apps.api_keys.tasks import create_apikey_snapshot
from apps.projects.forms import DomainForm
from apps.projects.models import Domain
from apps.projects.models import Project


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user.profile

        # Projects
        context["projects"] = Project.objects.filter(user=user_profile)

        # ---------- API Usage Over Time ----------
        last_30_days = timezone.now().date() - timedelta(days=30)
        usage = (
            APIUsageSummary.objects.filter(
                Q(api_key__project__user=user_profile)
                | Q(api_key__domain__project__user=user_profile),
                date__gte=last_30_days,
            )
            .values("date")
            .annotate(
                total_requests=Sum("total_requests"),
                success_requests=Sum("success_requests"),
                error_requests=Sum("error_requests"),
                api_key_name=F("api_key__name"),
            )
            .order_by("date")
        )
        usage_chart_data = {
            "dates": [u["date"].strftime("%Y-%m-%d") for u in usage],
            "total": [u["total_requests"] for u in usage],
            "success": [u["success_requests"] for u in usage],
            "errors": [u["error_requests"] for u in usage],
            "api": [u["api_key_name"] for u in usage.distinct()],
        }

        print(usage_chart_data["api"])

        # ---------- Top Endpoints ----------
        logs = (
            APIRequestLog.objects.filter(
                Q(project__user=user_profile)
                | Q(api_key__domain__project__user=user_profile)
                | Q(api_key__project__user=user_profile)
            )
            .annotate(
                endpoint_trimmed=Substr(F("endpoint"), 1, Length("endpoint") - 1),
                reversed_endpoint=Reverse(F("endpoint_trimmed")),
                slash_index=StrIndex(F("reversed_endpoint"), Value("/")),
                last_segment_reversed=Substr(
                    F("reversed_endpoint"), 1, F("slash_index") - 1
                ),
                resource=Reverse(F("last_segment_reversed")),
            )
            .values("resource")
            .annotate(total_requests=Count("id"))
            .order_by("-total_requests")[:10]
        )
        top_endpoints_chart_data = {
            "resources": [log["resource"].title() for log in logs],
            "counts": [log["total_requests"] for log in logs],
        }

        # Convert to JSON so template JS can parse without syntax errors
        context["usage_chart_data"] = json.dumps(usage_chart_data)
        context["top_endpoints_chart_data"] = json.dumps(top_endpoints_chart_data)

        return context


dashboard = DashboardView.as_view()


class DomainView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/pages/domains.html"
    form_class = DomainForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["domains"] = Domain.objects.filter(
            project__user=self.request.user.profile,
        )
        context["domain_form"] = self.form_class()
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            url = form.cleaned_data.get("url")
            try:
                response = requests.get(url, timeout=3)
                response.raise_for_status()
                form.save()
                return JsonResponse(
                    {
                        "message": "Domain is reachable. Enjoy",
                        "valid": True,
                        "status": response.status_code,
                        "next_url": str(reverse("dashboard:domains")),
                    },
                    status=201,
                )
            except requests.RequestException as e:
                return JsonResponse(
                    {"valid": False, "message": f"Domain could not be reached: {e!s}"},
                    status=400,
                )
        else:
            return JsonResponse(
                {"valid": False, "message": form.errors.as_text()}, status=400
            )


domains_view = DomainView.as_view()


class APIKEYView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/pages/api-keys.html"
    success_url = reverse_lazy("dashboard:apikeys")
    form_class = APIKeyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(profile=self.request.user.profile)
        context["apikeys"] = APIKey.objects.prefetch_related(
            "domain", "project"
        ).filter(
            Q(project__user=self.request.user.profile)
            | Q(domain__project__user=self.request.user.profile)
        )
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, profile=request.user.profile)
        if form.is_valid():
            instance = form.save()
            create_apikey_snapshot.delay(
                instance.uuid, request.user.profile.id, instance.raw_key
            )
            return JsonResponse(
                {
                    "message": f"{instance.raw_key}",
                    "valid": True,
                    "next_url": str(self.success_url),
                    "hold": True,
                    "is_secret_key": True,
                },
                status=201,
            )
        return JsonResponse(
            {"valid": False, "message": form.errors.as_text()}, status=400
        )


api_keys_view = APIKEYView.as_view()
