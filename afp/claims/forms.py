from datetime import datetime

from django import forms
from django.core.validators import RegexValidator
from django.forms.models import inlineformset_factory
from django.urls import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Div, Field, HTML, Layout, Submit

from afp.accounts.models import CustomUser
from .models import (
    Award,
    Cpa,
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
    Student,
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
            "ver_file",
            "ver_url",
            "comments",
        ]
        widgets = {
            "comments": forms.Textarea(attrs={"rows": 5}),
        }


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = [
            "promoted_to",
            "comments",
            "ver_file",
            "ver_url",
        ]


class BookForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = [
            "pub_type",
            "title",
            "authors",
            "chapter_title",
            "authors_contd",
            "publisher",
            "city",
            "isbn",
            "pub_year",
            "comments",
            "ver_file",
            "ver_url",
        ]

        widgets = {"comments": forms.Textarea(attrs={"rows": 5})}


class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = [
            "title",
            "authors",
            "conf_name",
            "city",
            "date",
            "comments",
            "ver_file",
            "ver_url",
        ]

        widgets = {"comments": forms.Textarea(attrs={"rows": 5})}


class JournalForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = [
            "title",
            "authors",
            "authors_contd",
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
            "comments",
            "ver_file",
            "ver_url",
        ]

        widgets = {"comments": forms.Textarea(attrs={"rows": 5})}


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
        widgets = {"comments": forms.Textarea(attrs={"rows": 5})}


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
        widgets = {"comments": forms.Textarea(attrs={"rows": 5})}


class GrantLinkForm(forms.ModelForm):
    class Meta:
        model = GrantLink
        fields = "__all__"


GrantLinkFormSet = inlineformset_factory(
    Grant,
    GrantLink,
    form=GrantLinkForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True,
)


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
            "num_reviewed",
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
                },
            ),
            "comments": forms.Textarea(attrs={"rows": 5}),
        }


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
        widgets = {"comments": forms.Textarea(attrs={"rows": 5})}


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
        widgets = {
            "start_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "min": datetime.strptime("01012022", "%d%m%Y").date(),
                    "max": datetime.strptime("31122022", "%d%m%Y").date(),
                },
            ),
            "end_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "min": datetime.strptime("01012022", "%d%m%Y").date(),
                    "max": datetime.strptime("31122022", "%d%m%Y").date(),
                },
            ),
            "comments": forms.Textarea(attrs={"rows": 5}),
        }


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = [
            "exam_type",
            "other_exam_name",
            "student",
            "date",
            "hours",
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
                },
            ),
            "comments": forms.Textarea(attrs={"rows": 5}),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "student_type",
            "other_student_type",
            "resident_year",
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
        widgets = {"comments": forms.Textarea(attrs={"rows": 5})}


class CpaForm(forms.ModelForm):
    class Meta:
        model = Cpa
        fields = ["cpa_file", "ver_file", "comments"]
        widgets = {"comments": forms.Textarea(attrs={"rows": 5})}
