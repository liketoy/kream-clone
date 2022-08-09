from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from core.utils import upload_to


class User(AbstractUser):

    """Custom User Model"""

    SHOE_SIZE_CHOICES = [
        ("220", "220"),
        ("225", "225"),
        ("230", "230"),
        ("235", "235"),
        ("240", "240"),
        ("245", "245"),
        ("250", "250"),
        ("255", "255"),
        ("260", "260"),
        ("265", "265"),
        ("270", "270"),
        ("275", "275"),
        ("280", "280"),
        ("285", "285"),
        ("290", "290"),
        ("295", "295"),
        ("300", "300"),
    ]

    avatar = models.ImageField(upload_to=upload_to("avatars", True), blank=True)
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone_number = models.CharField(
        validators=[phoneNumberRegex], max_length=16, unique=True
    )
    shoe_size = models.CharField(choices=SHOE_SIZE_CHOICES, max_length=3, blank=True)
    is_ad_message = models.BooleanField(default=False)
    is_ad_email = models.BooleanField(default=False)
