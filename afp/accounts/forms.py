from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import CustomUser, Physician


class ProfileUpdateForm(UserChangeForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "username",
            "email",
            "password",
            "date_joined",
            "division",
            "other_division",
            "rank",
        ]
