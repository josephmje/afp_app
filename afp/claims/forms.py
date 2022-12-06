from datetime import datetime

from django import forms
from django.forms.models import inlineformset_factory

from .models import (
    Award,
    CommitteeWork,
    Cpa,
    EditorialBoard,
    Exam,
    Grant,
    GrantLink,
    GrantReview,
    Lecture,
    Promotion,
    Publication,
    PublicationLink,
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
            "ver_file": forms.ClearableFileInput(
                attrs={
                    "accept": "application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, image/jpeg, image/png"
                }
            ),
            "comments": forms.Textarea(attrs={"rows": 5}),
        }


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = [
            "promoted_to",
            "ver_file",
            "ver_url",
            "comments",
        ]
        widgets = {
            "ver_file": forms.ClearableFileInput(
                attrs={
                    "accept": "application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, image/jpeg, image/png"
                }
            ),
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

        widgets = {
            "ver_file": forms.ClearableFileInput(
                attrs={
                    "accept": "application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, image/jpeg, image/png"
                }
            ),
            "comments": forms.Textarea(attrs={"rows": 5}),
        }


class PublicationLinkForm(forms.ModelForm):
    class Meta:
        model = PublicationLink
        fields = ["user_id", "role", "is_corresponding"]


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
        widgets = {
            "ver_file": forms.ClearableFileInput(
                attrs={
                    "accept": "application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, image/jpeg, image/png"
                }
            ),
            "comments": forms.Textarea(attrs={"rows": 5}),
        }

    def fields_required(self, fields):
        for field in fields:
            if not self.cleaned_data.get(field, ""):
                msg = forms.ValidationError("This field is required.")
                self.add_error(field, msg)

    def clean(self):
        journal = self.cleaned_data.get("journal")

        if journal == "Other":
            self.fields_required(["other_journal_name"])
        else:
            self.cleaned_data["other_journal_name"] = ""

        return self.cleaned_data


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
            "ver_file": forms.ClearableFileInput(
                attrs={
                    "accept": "application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, image/jpeg, image/png"
                }
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
            "ver_file": forms.ClearableFileInput(
                attrs={
                    "accept": "application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, image/jpeg, image/png"
                }
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
        widgets = {
            "ver_file": forms.ClearableFileInput(
                attrs={
                    "accept": "application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, image/jpeg, image/png"
                }
            ),
            "comments": forms.Textarea(attrs={"rows": 5}),
        }


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
            "ver_file": forms.ClearableFileInput(
                attrs={
                    "accept": "application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, image/jpeg, image/png"
                }
            ),
            "comments": forms.Textarea(attrs={"rows": 5}),
        }

    def fields_required(self, fields):
        for field in fields:
            if not self.cleaned_data.get(field, ""):
                msg = forms.ValidationError("This field is required.")
                self.add_error(field, msg)

    def clean(self):
        lecture_type = self.cleaned_data.get("lecture_type")
        is_series = self.cleaned_data.get("is_series")

        if lecture_type == "Other Lecture":
            self.fields_required(["other_lecture_type"])
        else:
            self.cleaned_data["other_lecture_type"] = ""

        if is_series:
            self.fields_required(["num_sessions"])
            self.fields_required(["end_date"])
        else:
            self.cleaned_data["num_sessions"] = 1
            self.cleaned_data["end_date"] = self.cleaned_data.get("start_date")

        return self.cleaned_data


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = [
            "exam_type",
            "other_exam_name",
            "student_name",
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
            "ver_file": forms.ClearableFileInput(
                attrs={
                    "accept": "application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, image/jpeg, image/png"
                }
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
            "student_name",
            "resident_year",
            "supervision_type",
            "hours",
            "duration",
            "frequency",
            "comments",
            "ver_file",
            "ver_url",
        ]
        widgets = {
            "ver_file": forms.ClearableFileInput(
                attrs={
                    "accept": "application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, image/jpeg, image/png"
                }
            ),
            "comments": forms.Textarea(attrs={"rows": 5}),
        }


class CpaForm(forms.ModelForm):
    class Meta:
        model = Cpa
        fields = ["cpa_file", "ver_file", "comments"]
        widgets = {
            "cpa_file": forms.ClearableFileInput(
                attrs={
                    "accept": "application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, image/jpeg, image/png"
                }
            ),
            "ver_file": forms.ClearableFileInput(
                attrs={
                    "accept": "application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, image/jpeg, image/png"
                }
            ),
            "comments": forms.Textarea(attrs={"rows": 5}),
        }
