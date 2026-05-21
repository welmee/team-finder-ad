from django import forms
from django.core.exceptions import ValidationError

from .models import Project


def validate_github_url(value):
    if value and "github.com" not in value:
        raise ValidationError("Ссылка должна вести на github.com.")


class ProjectForm(forms.ModelForm):
    github_url = forms.URLField(
        required=False,
        validators=[validate_github_url],
        label="Ссылка на GitHub",
    )
    status = forms.ChoiceField(
        choices=[("open", "Открыт"), ("closed", "Закрыт")],
        label="Статус",
    )

    class Meta:
        model = Project
        fields = ["name", "description", "github_url", "status"]
