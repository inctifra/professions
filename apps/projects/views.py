import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.base import View

from apps.projects.models import Project
from apps.subscriptions.utils import create_subscription_and_billing

from .forms import ProjectForm


class ProjectCreationView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/pages/projects/create.html"
    form_class = ProjectForm

    @property
    def profile(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(profile=self.profile)
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class(request.POST, profile=self.profile)
        if form.is_valid():
            instance = form.save(commit=True)
        else:
            return JsonResponse({"message": str(form.errors.as_text())}, safe=False)
        return JsonResponse(
            {
                "next_url": str(
                    reverse(
                        "dashboard:projects:checkout",
                        kwargs={"uuid": str(instance.uuid)},
                    ),
                ),
            },
            status=201,
            safe=False,
        )


create_project_view = ProjectCreationView.as_view()


class ProjectPurchaseUpdate(LoginRequiredMixin, View):
    form_class = ProjectForm

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(
            Project,
            user=self.request.user.profile,
            uuid=kwargs.get("uuid"),
        )
        form = self.form_class(
            request.POST,
            profile=self.request.user.profile,
            instance=project,
        )
        if form.is_valid():
            instance = form.save(commit=True)
        else:
            return JsonResponse(
                {"message": str(form.errors.as_text())},
                status=400,
                safe=False,
            )
        return JsonResponse(
            {
                "next_url": str(
                    reverse(
                        "dashboard:projects:checkout",
                        kwargs={"uuid": str(instance.uuid)},
                    ),
                ),
            },
            status=201,
            safe=False,
        )


update_project_purchase_view = ProjectPurchaseUpdate.as_view()


class ProjectCheckoutPageView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/pages/checkout/project.html"

    def get_context_data(self, **kwargs):
        project = get_object_or_404(
            Project,
            user=self.request.user.profile,
            uuid=kwargs.get("uuid"),
        )
        context = super().get_context_data(**kwargs)
        context["project"] = project
        context["project_form"] = ProjectForm(
            profile=self.request.user.profile,
            instance=project,
        )
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        project = get_object_or_404(
            Project,
            uuid=kwargs.get("uuid"),
            is_active=False,
            is_paid=False,
            user=request.user.profile,
        )

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "kes",
                        "unit_amount": int(project.plan.price * 100),
                        "product_data": {
                            "name": f"{project.plan.name} for {project.name}",
                            "description": f"Payment for project {project.name}",
                        },
                    },
                    "quantity": 1,
                },
            ],
            success_url=request.build_absolute_uri(
                reverse(
                    "dashboard:projects:payment_success",
                    kwargs={"uuid": str(project.uuid)},
                ),
            ),
            cancel_url=request.build_absolute_uri(
                reverse(
                    "dashboard:projects:payment_cancel",
                    kwargs={"uuid": str(project.uuid)},
                ),
            ),
            client_reference_id=str(project.uuid),
        )

        return JsonResponse({"next_url": checkout_session.url}, status=201, safe=False)


project_purchase_checkout = ProjectCheckoutPageView.as_view()


def project_purchase_success_view(request, uuid):
    project = get_object_or_404(Project, uuid=uuid)
    subscription = create_subscription_and_billing(project)
    return redirect("dashboard:home")
    return render(
        request,
        "dashboard/pages/projects/payments/success.html",
        {"project": project, "subscription": subscription},
    )


def project_purchase_cancel_view(request, uuid):
    return render(request, "dashboard/pages/projects/payments/cancel.html")
