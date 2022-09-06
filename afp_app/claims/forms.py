from afp_app.claims.models import Award
from django import forms


class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = [
            "name",
            "organization",
            "award_level",
            "cash_prize",
            "comments",
            "ver_file",
            "ver_url",
        ]
