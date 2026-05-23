from django.core.exceptions import ValidationError

GITHUB_HOST = "github.com"


def validate_github_url(value):
    if value and GITHUB_HOST not in value:
        raise ValidationError("Ссылка должна вести на github.com.")
