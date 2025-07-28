from django.db import models
from django.contrib.auth.hashers import (
    make_password,
    check_password as dj_check_password,
)

from .validators import validate_strong_password


class CustomUserModel(models.Model):
    name = models.CharField(max_length=255, default="", blank=True)
    surname = models.CharField(max_length=255, default="", blank=True)
    phone_number = models.CharField(max_length=20, default="", unique=True)
    password = models.CharField(max_length=65, validators=[validate_strong_password])
    profile_image = models.ImageField(upload_to="user/", null=True, blank=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["phone_number", "password"]

    def set_password(self, raw_password: str) -> None:
        self.password = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return dj_check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        if self.password and "$" not in self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
