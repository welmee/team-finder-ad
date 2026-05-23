from django.contrib.auth.models import BaseUserManager

from .utils import AVATAR_DEFAULT_LETTER, generate_avatar


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("phone", "")
        user = self.model(email=email, name=name, surname=surname, **extra_fields)
        user.set_password(password)
        letter = name[0] if name else AVATAR_DEFAULT_LETTER
        avatar_content = generate_avatar(letter)
        safe_email = email.replace("@", "_at_")
        user.avatar.save(f"avatar_{safe_email}.png", avatar_content, save=False)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, name, surname, password, **extra_fields)
