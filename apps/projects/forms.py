from django import forms

from apps.projects.models import Domain
from apps.projects.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "plan"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter project name"},
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Describe your project (optional)",
                    "rows": 3,
                },
            ),
            "plan": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop("profile", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=...):
        instance = super().save(commit=False)
        if self.profile:
            instance.user = self.profile
        if commit:
            instance.save()
        return instance


class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = ["project", "name", "url"]
        widgets = {
            "project": forms.Select(attrs={"class": "form-control"}),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter domain name (e.g., example.com)",
                },
            ),
            "url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Full URL (e.g., https://example.com)",
                },
            ),
        }
