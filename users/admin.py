from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):

    """Custom User Admin"""

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "phone_number",
                    "shoe_size",
                    "is_ad_message",
                    "is_ad_email",
                )
            },
        ),
    )
