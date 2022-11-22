from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import CustomUser, Physician


class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "division",
            "other_division",
            "rank",
        ]
