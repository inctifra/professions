from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg
from django.db.models import Q
from django.db.models import QuerySet
from django.db.models import Sum
from django.db.models import Count
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from apps.analytics.models import APIUsageSummary
from apps.projects.models import Project
from professions.users.models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = "dashboard/users/profile.html"
    model = User
    context_object_name = "profile"

    def get_object(self, queryset=...):
        return self.request.user

    def get_user_project_plan(self):
        project = (
            Project.objects.filter(user=self.get_object().profile)
            .select_related("plan")
            .first()
        )
        if project and project.plan:
            subscription = getattr(project, "subscription", None)
            renewal_date = subscription.end_date if subscription else None
            return {
                "price": project.plan.price,
                "name": project.plan.get_name_display(),
                "project": project.name,
                "renewal_date": renewal_date.isoformat() if renewal_date else None,
            }
        return None
    def get_user_api_stats(self):
        return (
            APIUsageSummary.objects.filter(
                Q(api_key__project__user=self.get_object().profile) |
                Q(api_key__domain__project__user=self.get_object().profile)
            )
            .aggregate(
                total_requests=Sum("total_requests"),
                success_requests=Sum("success_requests"),
                error_requests=Sum("error_requests"),
                avg_latency_ms=Avg("avg_latency_ms"),
                total_projects=Count("api_key__project", distinct=True),
                total_domains=Count("api_key__domain", distinct=True),
            )
        )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_project_plan"] = self.get_user_project_plan()
        context["user_api_stats"] = self.get_user_api_stats()
        return context


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None = None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()
