from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from team_finder.validators import validate_github_url

from .constants import NAME_MAX_LENGTH, SURNAME_MAX_LENGTH
from .utils import normalize_phone

User = get_user_model()


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=NAME_MAX_LENGTH, label="Имя")
    surname = forms.CharField(max_length=SURNAME_MAX_LENGTH, label="Фамилия")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def save(self):
        return User.objects.create_user(
            email=self.cleaned_data["email"],
            name=self.cleaned_data["name"],
            surname=self.cleaned_data["surname"],
            password=self.cleaned_data["password"],
        )


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")


class EditProfileForm(forms.ModelForm):
    github_url = forms.URLField(
        required=False,
        validators=[validate_github_url],
        label="GitHub",
    )

    class Meta:
        model = User
        fields = ["name", "surname", "avatar", "about", "phone", "github_url"]

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "")
        exclude_pk = self.instance.pk if self.instance and self.instance.pk else None
        return normalize_phone(
            phone,
            exclude_user_pk=exclude_pk,
            user_model=User,
        )


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Старый пароль")
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="Новый пароль")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Подтвердите новый пароль")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old = self.cleaned_data.get("old_password")
        if not self.user.check_password(old):
            raise ValidationError("Старый пароль введён неверно.")
        return old

    def clean(self):
        cleaned = super().clean()
        password1 = cleaned.get("new_password1")
        password2 = cleaned.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Новые пароли не совпадают.")
        return cleaned
