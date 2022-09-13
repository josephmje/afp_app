from afp_app.accounts.models import CustomUser
from afp_app.claims.models import (
    Award,
    Promotion,
    Grant,
    GrantReview,
    Publication,
    EditorialBoard,
    Lecture,
    Exam,
    Supervision,
)
from django import forms


class ProfileForm(forms.ModelForm):
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


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = [
            "promoted_to",
            "comments",
            "ver_file",
            "ver_url",
        ]
