from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
import requests

from professions.api_keys.models import APIKey
from professions.projects.forms import DomainForm
from professions.projects.models import Domain
from professions.projects.models import Project
from professions.api_keys.forms import APIKeyForm
from django.db.models import Q

@login_required
def dashboard(request):
    """
    Render the dashboard view.
    """
    projects = Project.objects.filter(user=request.user.profile)
    context = {"projects": projects}
    return render(request, "dashboard/home.html", context)


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
        context["apikeys"] = APIKey.objects.prefetch_related("domain", "project").filter(
            Q(project__user=self.request.user.profile) |
            Q(domain__project__user=self.request.user.profile)
        )
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, profile=request.user.profile)
        if form.is_valid():
            instance = form.save()
            return JsonResponse(
                {
                    "message": f"{instance.raw_key}",
                    "valid": True,
                    "next_url": str(self.success_url),
                },
                status=201,
            )
        return JsonResponse(
            {"valid": False, "message": form.errors.as_text()}, status=400
        )


api_keys_view = APIKEYView.as_view()
