import re

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


def validate_github_url(value):
    if value and "github.com" not in value:
        raise ValidationError("Ссылка должна вести на github.com.")


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=124, label="Имя")
    surname = forms.CharField(max_length=124, label="Фамилия")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")


class EditProfileForm(forms.ModelForm):
    github_url = forms.URLField(required=False, validators=[validate_github_url], label="GitHub")

    class Meta:
        model = User
        fields = ["name", "surname", "avatar", "about", "phone", "github_url"]

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if not phone:
            raise ValidationError("Телефон обязателен для заполнения.")
        if phone.startswith("+7"):
            phone = "8" + phone[2:]
        elif phone.startswith("8"):
            pass
        else:
            raise ValidationError(
                "Телефон должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX."
            )
        if not re.match(r"^8\d{10}$", phone):
            raise ValidationError(
                "Телефон должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX."
            )
        qs = User.objects.filter(phone=phone)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Этот номер телефона уже используется другим пользователем.")
        return phone


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
        p1 = cleaned.get("new_password1")
        p2 = cleaned.get("new_password2")
        if p1 and p2 and p1 != p2:
            raise ValidationError("Новые пароли не совпадают.")
        return cleaned
