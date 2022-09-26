from django import forms
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse

from afp.accounts.models import CustomUser, Division, Physician, Rank


class CustomUserCreationForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    class Meta:
        model = CustomUser
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
        model = CustomUser
        fields = "__all__"


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()


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

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("upload-csv/", self.upload_csv),
        ]
        return new_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith(".csv"):
                messages.warning(request, "The wrong file type was uploaded.")
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data:
                fields = x.split(",")
                created = CustomUser.objects.update_or_create(
                    id=fields[0],
                    first_name=fields[1],
                    middle_name=fields[2],
                    last_name=fields[3],
                    email=fields[4],
                    username=fields[5],
                    password=fields[6],
                    is_staff=fields[7],
                    is_active=fields[8],
                    is_physician=fields[9],
                    is_scientist=fields[10],
                    division=fields[11],
                    rank=fields[12],
                )
            url = reverse("admin:index")
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "csv_upload.html", data)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Physician)
admin.site.register(Division)
admin.site.register(Rank)
