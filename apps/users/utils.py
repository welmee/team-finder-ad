import io
import random
import re

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

AVATAR_COLOR_BLUE = "#4f86c6"
AVATAR_COLOR_GREEN = "#5ba35b"
AVATAR_COLOR_ORANGE = "#c47f3b"
AVATAR_COLOR_PURPLE = "#9b59b6"
AVATAR_COLOR_TEAL = "#2e86ab"
AVATAR_COLOR_AMBER = "#e07b39"
AVATAR_COLOR_FOREST = "#3b7a57"
AVATAR_COLOR_RED = "#c0392b"
AVATAR_COLOR_TURQUOISE = "#1abc9c"
AVATAR_COLOR_VIOLET = "#8e44ad"
AVATAR_COLOR_STEEL_BLUE = "#2980b9"
AVATAR_COLOR_EMERALD = "#27ae60"

AVATAR_COLORS = [
    AVATAR_COLOR_BLUE,
    AVATAR_COLOR_GREEN,
    AVATAR_COLOR_ORANGE,
    AVATAR_COLOR_PURPLE,
    AVATAR_COLOR_TEAL,
    AVATAR_COLOR_AMBER,
    AVATAR_COLOR_FOREST,
    AVATAR_COLOR_RED,
    AVATAR_COLOR_TURQUOISE,
    AVATAR_COLOR_VIOLET,
    AVATAR_COLOR_STEEL_BLUE,
    AVATAR_COLOR_EMERALD,
]

FONT_PATH_DEBIAN = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_PATH_MACOS = "/System/Library/Fonts/Helvetica.ttc"

FONT_PATHS = [
    FONT_PATH_DEBIAN,
    FONT_PATH_MACOS,
]

AVATAR_SIZE = 200
AVATAR_FONT_SIZE = 100
AVATAR_TEXT_COLOR = "white"
AVATAR_FILENAME = "avatar.png"
AVATAR_DEFAULT_LETTER = "U"

PHONE_DIGITS_COUNT = 10
PHONE_PREFIX_RU = "8"
PHONE_PREFIX_INTL = "+7"

MSG_PHONE_REQUIRED = "Телефон обязателен для заполнения."
MSG_PHONE_INVALID_FORMAT = (
    "Телефон должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX."
)
MSG_PHONE_ALREADY_USED = "Этот номер телефона уже используется другим пользователем."


def normalize_phone(phone, *, exclude_user_pk=None, user_model=None):
    phone = phone.strip()
    if not phone:
        raise ValidationError(MSG_PHONE_REQUIRED)

    if phone.startswith(PHONE_PREFIX_INTL):
        phone = PHONE_PREFIX_RU + phone[len(PHONE_PREFIX_INTL):]
    elif phone.startswith(PHONE_PREFIX_RU):
        pass
    else:
        raise ValidationError(MSG_PHONE_INVALID_FORMAT)

    if not re.match(rf"^{PHONE_PREFIX_RU}\d{{{PHONE_DIGITS_COUNT}}}$", phone):
        raise ValidationError(MSG_PHONE_INVALID_FORMAT)

    if user_model is not None:
        qs = user_model.objects.filter(phone=phone)
        if exclude_user_pk is not None:
            qs = qs.exclude(pk=exclude_user_pk)
        if qs.exists():
            raise ValidationError(MSG_PHONE_ALREADY_USED)

    return phone


def generate_avatar(letter: str) -> ContentFile:
    color = random.choice(AVATAR_COLORS)
    img = Image.new("RGB", (AVATAR_SIZE, AVATAR_SIZE), color=color)
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    for path in FONT_PATHS:
        try:
            font = ImageFont.truetype(path, size=AVATAR_FONT_SIZE)
            break
        except OSError:
            continue
    text = letter.upper()
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    draw.text(
        (
            (AVATAR_SIZE - width) / 2 - bbox[0],
            (AVATAR_SIZE - height) / 2 - bbox[1],
        ),
        text,
        fill=AVATAR_TEXT_COLOR,
        font=font,
    )
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return ContentFile(buffer.getvalue(), name=AVATAR_FILENAME)
