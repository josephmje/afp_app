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
