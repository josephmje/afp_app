from datetime import datetime

from django import forms
from django.forms.models import inlineformset_factory
from django.urls import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from afp.accounts.models import CustomUser
from .models import (
    Award,
    CommitteeWork,
    EditorialBoard,
    Exam,
    Grant,
    GrantLink,
    Publication,
    PublicationLink,
    GrantReview,
    Lecture,
    Promotion,
    Supervision,
)


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy("add_award")
        self.helper.form_method = "POST"
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


class GrantForm(forms.ModelForm):
    class Meta:
        model = Grant
        fields = [
            "name",
            "agency",
            "other_grant_agency",
            "pi_list",
            "coi_list",
            "start_date",
            "end_date",
            "at_camh",
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
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "min": datetime.strptime("01012022", "%d%m%Y").date(),
                    "max": datetime.strptime("31122022", "%d%m%Y").date(),
                }
            )
        }


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = [
            "pub_type",
            "authors",
            "title",
            "publisher",
            "isbn",
            "article_type",
            "journal",
            "other_journal_name",
            "volume",
            "issue",
            "start_page",
            "end_page",
            "pub_month",
            "pub_year",
            "pmid",
            "other_impact_factor",
            "is_epub",
            "conf_name",
            "location",
            "comments",
            "ver_file",
            "ver_url",
        ]


PublicationLinkFormSet = inlineformset_factory(
    Publication,
    PublicationLink,
    form=PublicationForm,
    can_delete=True,
    min_num=1,
    extra=0,
)


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


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
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


class SupervisionForm(forms.ModelForm):
    class Meta:
        model = Supervision
        fields = [
            "student_id",
            "supervision_type",
            "hours",
            "duration",
            "med_duration",
            "frequency",
            "comments",
            "ver_file",
            "ver_url",
        ]
