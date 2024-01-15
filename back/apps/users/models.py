from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("instructor", "Instructor"),
        ("user", "User"),
        ("jablicko", "Jablicko"),
        # Další role, jak potřebuješ
    )

    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    email_is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    adress = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
