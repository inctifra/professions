from typing import Any

from django.views.generic.base import TemplateView

from professions.core.forms import ProfessionModelSelectForm


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_professions_search_form(self, **kwargs):
        return ProfessionModelSelectForm(
            app_label="professions_reader", data=self.request.GET or None
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
