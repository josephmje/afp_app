from datetime import datetime

from django import forms
from django.forms.models import inlineformset_factory


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
    Student,
    Supervision,
)


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


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = [
            "pub_type",
            "title",
            "chapter_title",
            "authors",
            "chapter_authors",
            "publisher",
            "city",
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
            "is_epub",
            "conf_name",
            "conf_date",
            "comments",
            "ver_file",
            "ver_url",
        ]

        widgets = {"comments": forms.Textarea(attrs={"rows": 5})}


class PublicationLinkForm(forms.ModelForm):
    class Meta:
        model = PublicationLink
        fields = ["user_id", "role"]


PublicationLinkFormSet = inlineformset_factory(
    Publication,
    PublicationLink,
    form=PublicationLinkForm,
    extra=0,
    min_num=1,
    can_delete=True,
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
        widgets = {"comments": forms.Textarea(attrs={"rows": 5})}


class GrantForm(forms.ModelForm):
    class Meta:
        model = Grant
        fields = [
            "name",
            "pi_list",
            "coi_list",
            "agency",
            "other_grant_agency",
            "amount",
            "start_date",
            "end_date",
            "at_camh",
            "comments",
            "ver_file",
            "ver_url",
        ]
        widgets = {
            "start_date": forms.DateInput(
                attrs={
                    "type": "date",
                },
            ),
            "end_date": forms.DateInput(
                attrs={
                    "type": "date",
                },
            ),
            "comments": forms.Textarea(attrs={"rows": 5}),
        }


class GrantLinkForm(forms.ModelForm):
    class Meta:
        model = GrantLink
        fields = ["user_id", "role"]


GrantLinkFormSet = inlineformset_factory(
    Grant,
    GrantLink,
    fields=("user_id", "role"),
    form=GrantLinkForm,
    extra=0,
    min_num=1,
    can_delete=True,
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
            "other_student_name",
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
            "other_student_name",
            "supervision_type",
            "hours",
            "duration",
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
