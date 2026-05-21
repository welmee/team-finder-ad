import io
import random

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont


AVATAR_COLORS = [
    "#4f86c6", "#5ba35b", "#c47f3b", "#9b59b6",
    "#2e86ab", "#e07b39", "#3b7a57", "#c0392b",
    "#1abc9c", "#8e44ad", "#2980b9", "#27ae60",
]

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]


def generate_avatar(letter: str) -> ContentFile:
    size = 200
    color = random.choice(AVATAR_COLORS)
    img = Image.new("RGB", (size, size), color=color)
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    for path in FONT_PATHS:
        try:
            font = ImageFont.truetype(path, size=100)
            break
        except OSError:
            continue
    text = letter.upper()
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(
        ((size - w) / 2 - bbox[0], (size - h) / 2 - bbox[1]),
        text,
        fill="white",
        font=font,
    )
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return ContentFile(buf.getvalue(), name="avatar.png")


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("phone", "")
        user = self.model(email=email, name=name, surname=surname, **extra_fields)
        user.set_password(password)
        avatar_content = generate_avatar(name[0] if name else "U")
        safe_email = email.replace("@", "_at_")
        user.avatar.save(f"avatar_{safe_email}.png", avatar_content, save=False)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, name, surname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    avatar = models.ImageField(upload_to="avatars/")
    phone = models.CharField(max_length=12, default="")
    github_url = models.URLField(blank=True)
    about = models.TextField(max_length=256, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.name} {self.surname} <{self.email}>"
