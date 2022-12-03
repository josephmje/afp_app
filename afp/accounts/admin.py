from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from afp.accounts.models import Division, Physician, Rank

User = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    class Meta:
        model = User
        fields = (
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "is_active",
            "is_staff",
            "is_physician",
            "is_scientist",
            "division",
            "other_division",
            "rank",
        )


class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    class Meta:
        model = User
        fields = "__all__"


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "middle_name",
                    "last_name",
                    "email",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_physician",
                    "is_scientist",
                )
            },
        ),
        (
            "Miscellaneous",
            {"fields": ("division", "other_division", "rank")},
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Physician)
admin.site.register(Division)
admin.site.register(Rank)
