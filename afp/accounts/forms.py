from django import forms
from django.contrib.auth.forms import UserChangeForm

from .models import CustomUser


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
            "email",
            "division",
            "other_division",
            "rank",
        ]
