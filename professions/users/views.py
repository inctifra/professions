from allauth.account.views import LoginView as AllauthLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.http import JsonResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from professions.users.forms import UserLoginForm
from professions.users.models import User
from django.shortcuts import resolve_url


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


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


class LoginView(AllauthLoginView):
    form_class = UserLoginForm

    def form_valid(self, form):
        form.login(self.request, redirect_url=self.get_success_url())
        return JsonResponse({"success": True, "redirect_url": self.get_success_url()})

    def get_success_url(self):
        # Check if "next" parameter is present in GET or POST data,
        # else fallback to home page
        next_url = self.request.GET.get("next") or self.request.POST.get("next")
        if next_url:
            return next_url
        return resolve_url("/")

    def form_invalid(self, form):
        errors = form.non_field_errors()
        error_message = errors.as_text() if errors else "Invalid login credentials."
        return JsonResponse(
            {
                "success": False,
                "errors": error_message,
            },
            status=400,
        )

    def post(self, request: HttpRequest, *args, **kwargs):
        form = self.form_class(data=request.POST, request=request)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)
