from django import forms
from django.apps import apps


class ProfessionModelSelectForm(forms.Form):
    model = forms.ChoiceField(label="Select A profession", choices=[])

    def __init__(self, app_label, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_label = app_label
        self.fields["model"].choices = [
            (f"{app_label}.{model.__name__}", model._meta.verbose_name.title())  # noqa: SLF001
            for model in apps.get_app_config(app_label).get_models()
        ]

    def get_selected_model(self):
        """
        Returns the actual model class from the selected string value.
        """
        model_str = self.cleaned_data.get("model")
        if model_str:
            app_label, model_name = model_str.split(".")
            return apps.get_model(app_label, model_name)
        return None
