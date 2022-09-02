from afp_app.accounts.models import CustomUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

fields = list(UserAdmin.fieldsets)
fields[1] = (
    "Personal Info",
    {"fields": ("first_name", "middle_name", "last_name", "email")},
)
UserAdmin.fieldsets = tuple(fields)

admin.site.register(CustomUser, UserAdmin)
