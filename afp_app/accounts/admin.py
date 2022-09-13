from afp_app.accounts.models import CustomUser, Rank, Division
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


fields = list(UserAdmin.fieldsets)
fields[1] = (
    "Personal Info",
    {
        "fields": (
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "is_physician",
            "is_scientist",
            "division",
            "other_division",
            "rank",
        )
    },
)

UserAdmin.fieldsets = tuple(fields)

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Division)
admin.site.register(Rank)
