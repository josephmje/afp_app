from datetime import datetime

from django import forms
from django.urls import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from afp_app.accounts.models import User
from afp_app.claims.models import (
    Award,
    CommitteeWork,
    EditorialBoard,
    GrantReview,
    Lecture,
    Promotion,
)


class ProfileForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "award-form"
        self.helper.attrs = {
            "hx-post": reverse_lazy("add_award"),
            "hx-target": "#award-form",
            "hx-swap": "outerHTML",
        }
        self.helper.add_input(Submit("submit", "Submit"))


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = [
            "promoted_to",
            "comments",
            "ver_file",
            "ver_url",
        ]


class GrantReviewForm(forms.ModelForm):
    class Meta:
        model = GrantReview
        fields = [
            "type",
            "agency",
            "name",
            "date",
            "is_member",
            "num_days",
            "comments",
            "ver_file",
            "ver_url",
        ]


class EditorialBoardForm(forms.ModelForm):
    class Meta:
        model = EditorialBoard
        fields = [
            "journal",
            "other_journal_name",
            "comments",
            "ver_file",
            "ver_url",
        ]


class CommitteeWorkForm(forms.ModelForm):
    class Meta:
        model = CommitteeWork
        fields = [
            "name",
            "hours",
            "comments",
            "ver_file",
            "ver_url",
        ]


class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = [
            "lecture_type",
            "other_lecture_type",
            "name",
            "course_code",
            "start_date",
            "hours",
            "is_cash",
            "is_series",
            "end_date",
            "num_sessions",
            "comments",
            "ver_file",
            "ver_url",
        ]
