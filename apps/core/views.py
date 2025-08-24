from typing import Any

from django.contrib.auth.decorators import login_not_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from apps.core.forms import ProfessionModelSelectForm
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .models import MaintenanceSubscriber
from django.contrib import messages


class HomeView(TemplateView):
    template_name = "client/pages/home.html"

    @method_decorator(login_not_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_professions_search_form(self, **kwargs):
        return ProfessionModelSelectForm(
            app_label="professions_reader",
            data=self.request.GET or None,
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_professions_search_form(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        form = self.get_professions_search_form(**kwargs)

        selected_model = None
        queryset = None
        if form.is_valid():
            selected_model = form.get_selected_model()
            queryset = selected_model.objects.all() if selected_model else []
        context = self.get_context_data(**kwargs)
        context["queryset"] = queryset
        context["selected_model"] = selected_model
        return super().get(request, *args, **kwargs)


@require_POST
def join_waitlist(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            subscriber, created = MaintenanceSubscriber.objects.get_or_create(
                email=email
            )
            messages.success(request, "Thanks! We will notify you when we are back.")
    return redirect("/")
