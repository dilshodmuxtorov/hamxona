from django.contrib import admin
from .models import UserModel, OTP


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "surname",
        "phone_number",
        "role",
        "passport_number",
        "pinfll",
        "date_of_birth",
    )
    list_filter = ("role",)
    search_fields = ("name", "surname", "phone_number", "passport_number", "pinfll")
    readonly_fields = ("password", "role")
    ordering = ("id",)

    fieldsets = (
        (
            "Personal Info",
            {
                "fields": (
                    "name",
                    "surname",
                    "phone_number",
                    "password",
                    "profile_image",
                    "date_of_birth",
                )
            },
        ),
        ("Identification", {"fields": ("passport_number", "pinfll")}),
    )


admin.site.register(OTP)
