from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileUpdateForm(UserChangeForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    class Meta(UserChangeForm.Meta):
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
