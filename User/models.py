from django.db import models
from django.contrib.auth.hashers import (
    make_password,
    check_password as dj_check_password,
)
from django.utils import timezone
import datetime


from .validators import validate_strong_password


class CustomUserModel(models.Model):
    ROLES = [
        ("user", "User"),
        ("admin", "Admin"),
        ("university_admin", "University Admin"),
        ("dormitory_admin", "Dormitory Admin"),
        ("dormitory_master", "Dormitory Masters"),
    ]
    name = models.CharField(max_length=255, default="", blank=True)
    surname = models.CharField(max_length=255, default="", blank=True)
    phone_number = models.CharField(max_length=20, default="", unique=True)
    password = models.CharField(max_length=65, validators=[validate_strong_password])
    profile_image = models.ImageField(upload_to="user/", null=True, blank=True)
    role = models.CharField(choices=ROLES, max_length=25, default="user")

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

    def __str__(self):
        return self.name + " " + self.surname


class UserModel(CustomUserModel):
    passport_number = models.CharField(max_length=9, default="", unique=True)
    pinfll = models.CharField(max_length=14, default="", unique=True)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return super().__str__()

    def save(self, *args, **kwargs):
        self.role = "user"
        super().save(*args, **kwargs)

class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + datetime.timedelta(minutes=5)
