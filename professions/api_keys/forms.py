from django import forms

from professions.projects.models import Domain
from professions.projects.models import Project

from .models import APIKey

PERMISSION_CHOICES = [
    ("manage_project", "Manage Project"),
    ("manage_domain", "Manage Domain"),
]


class APIKeyForm(forms.ModelForm):
    permission_type = forms.ChoiceField(
        choices=PERMISSION_CHOICES,
        widget=forms.RadioSelect,
        label="Permission Type",
        initial="manage_project",
    )
    access_type = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = APIKey
        fields = ["name", "permission_type", "project", "domain", "access_type"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter API Key name"}
            ),
            "project": forms.Select(attrs={"class": "form-control"}),
            "domain": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop("profile", None)
        super().__init__(*args, **kwargs)
        self.fields["project"].queryset = Project.objects.filter(user=self.profile)
        self.fields["domain"].queryset = Domain.objects.filter(
            project__user=self.profile
        )
        self.fields["project"].required = False
        self.fields["domain"].required = False

    def clean(self):
        cleaned_data = super().clean()
        permission_type = cleaned_data.get("permission_type")
        if permission_type == "manage_project":
            cleaned_data["access_type"] = "project"
        else:
            cleaned_data["access_type"] = "domain"
        return cleaned_data
