from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from operator_api.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "groups",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {"fields": ("is_staff", "is_active", "apartments", "groups")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "groups",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
