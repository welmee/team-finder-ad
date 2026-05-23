from django import forms

from team_finder.validators import validate_github_url

from .constants import PROJECT_STATUS_CLOSED, PROJECT_STATUS_OPEN
from .models import Project


class ProjectForm(forms.ModelForm):
    github_url = forms.URLField(
        required=False,
        validators=[validate_github_url],
        label="Ссылка на GitHub",
    )
    status = forms.ChoiceField(
        choices=[
            (PROJECT_STATUS_OPEN, "Открыт"),
            (PROJECT_STATUS_CLOSED, "Закрыт"),
        ],
        label="Статус",
    )

    class Meta:
        model = Project
        fields = ["name", "description", "github_url", "status"]
