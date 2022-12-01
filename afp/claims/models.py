import uuid

from django import forms
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import filesizeformat
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from djmoney.models.fields import MoneyField

from afp.accounts.models import Rank

from .mixins import AdminMixin, CreatedUpdatedMixin

STR_SHORT = 10
STR_MED = 50
STR_LONG = 100
STR_LONGEST = 255


class BaseModel(AdminMixin, CreatedUpdatedMixin):
    """Model representing a base class."""

    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )
    comments = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class UserBaseModel(BaseModel):
    """Model extending the base class to log the user."""

    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


class ContentTypeRestrictedFileField(models.FileField):
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types", [])
        self.max_upload_size = kwargs.pop("max_upload_size", 0)
        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(
            *args, **kwargs
        )
        file = data.file
        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file.size > self.max_upload_size:
                    raise forms.ValidationError(
                        _(
                            "Please keep file size under %s. Current file size is %s"
                        )
                        % (
                            filesizeformat(self.max_upload_size),
                            filesizeformat(file.size),
                        )
                    )
            else:
                raise forms.ValidationError("This file type is not supported.")
        except AttributeError:
            pass
        return data


class AwardLevel(models.Model):
    """
    Model representing an award level and it's associated point value.
    """

    name = models.CharField(
        "Award Level",
        max_length=STR_MED,
        help_text="Enter an award level (e.g. Local, Hospital, etc.)",
        unique=True,
    )
    value = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(3000)]
    )

    def __str__(self):
        return self.name


class Award(UserBaseModel):
    """Model representing an award."""

    name = models.CharField("Award Name", max_length=STR_MED)
    organization = models.CharField(max_length=STR_MED)
    award_level = models.ForeignKey(
        AwardLevel,
        verbose_name="Award Level",
        on_delete=models.PROTECT,
        related_name="award_level",
    )
    cash_prize = models.BooleanField(
        default=False, verbose_name="Did you receive a cash prize?"
    )
    ver_file = ContentTypeRestrictedFileField(
        "Verification File",
        upload_to="uploads/awards/",
        content_types=[
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "image/jpeg",
            "image/png",
        ],
        max_upload_size=2621440,
        blank=True,
        null=True,
    )
    ver_url = models.URLField("Verification URL", blank=True, null=True)

    class Meta:
        ordering = ["award_level", "name"]

    def get_absolute_url(self):
        return reverse("award-detail", args=[str(self.id)])

    def __str__(self):
        return self.name


class Promotion(UserBaseModel):
    promoted_to = models.ForeignKey(Rank, on_delete=models.PROTECT)
    ver_file = ContentTypeRestrictedFileField(
        "Verification File",
        upload_to="uploads/promotions/",
        content_types=[
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "image/jpeg",
            "image/png",
        ],
        max_upload_size=2621440,
        blank=True,
        null=True,
    )
    ver_url = models.URLField("Verification URL", blank=True, null=True)


class GrantAgencyType(models.Model):
    name = models.CharField(
        max_length=STR_MED,
        help_text="Enter a grant agency type.",
        unique=True,
    )

    def __str__(self):
        return self.name


class GrantCategory(models.Model):
    name = models.CharField(
        max_length=STR_MED,
        help_text="Enter a grant category.",
        unique=True,
    )
    weight = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)],
    )

    class Meta:
        verbose_name_plural = "Grant categories"

    def __str__(self):
        return self.name


class GrantAgency(models.Model):
    name = models.CharField(
        max_length=STR_MED,
        help_text="Enter a grant agency type.",
    )
    type = models.ForeignKey(GrantAgencyType, on_delete=models.PROTECT)
    category = models.ForeignKey(GrantCategory, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Grant agencies"

    def __str__(self):
        return self.name


class Grant(BaseModel):
    amount = MoneyField(
        max_digits=14, decimal_places=2, default_currency="CAD"
    )
    name = models.CharField("Grant Title", max_length=STR_LONGEST)
    agency = models.ForeignKey(
        GrantAgency, on_delete=models.PROTECT, verbose_name="Granting Agency"
    )
    other_grant_agency = models.CharField(
        "Other Agency",
        max_length=STR_MED,
        blank=True,
        null=True,
        help_text="Only required if 'Other' is selected from the Grant Agency list.",
    )
    pi_list = models.CharField("List of PIs", max_length=STR_LONGEST)
    coi_list = models.CharField("List of Co-Is", max_length=STR_LONGEST)
    start_date = models.DateField()
    end_date = models.DateField()
    at_camh = models.BooleanField("Grant administered at CAMH?", default=False)
    ver_file = ContentTypeRestrictedFileField(
        "Verification File",
        upload_to="uploads/grants/",
        content_types=[
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "image/jpeg",
            "image/png",
        ],
        max_upload_size=2621440,
        blank=True,
        null=True,
    )
    ver_url = models.URLField("Verification URL", blank=True, null=True)

    def get_absolute_url(self):
        return reverse("view_grant", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class GrantRole(models.Model):
    name = models.CharField(
        max_length=STR_MED,
        help_text="Enter a grant role.",
        unique=True,
    )
    weight = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(7)],
    )

    def __str__(self):
        return self.name


class GrantLink(AdminMixin, CreatedUpdatedMixin):
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Investigator",
    )
    grant = models.ForeignKey(Grant, on_delete=models.CASCADE)
    role = models.ForeignKey(
        GrantRole, on_delete=models.PROTECT, verbose_name="Investigator Role"
    )
    entry_type = None


class GrantReviewType(models.Model):
    name = models.CharField(
        "Review Committee Type",
        max_length=STR_MED,
        unique=True,
    )
    weight = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(2000)]
    )

    def __str__(self):
        return self.name


class GrantReview(UserBaseModel):
    type = models.ForeignKey(
        GrantReviewType,
        verbose_name="Grant Review Type",
        on_delete=models.PROTECT,
    )
    agency = models.CharField("Granting Agency", max_length=STR_LONG)
    name = models.CharField(
        "Grant Name", max_length=STR_LONG, blank=True, null=True
    )
    date = models.DateField()
    is_member = models.BooleanField(
        default=False,
        verbose_name="Are you a full member of this grant review committee?",
        help_text="(only applies to external committees)",
    )
    num_days = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(25)],
        verbose_name="# Days Attended",
    )
    num_reviewed = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(99)],
        verbose_name="# Grants Reviewed",
    )
    ver_file = ContentTypeRestrictedFileField(
        "Verification File",
        upload_to="uploads/grant_reviews/",
        content_types=[
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "image/jpeg",
            "image/png",
        ],
        max_upload_size=2621440,
        blank=True,
        null=True,
    )
    ver_url = models.URLField("Verification URL", blank=True, null=True)


class PublicationType(models.Model):
    name = models.CharField(
        max_length=STR_MED,
        help_text="Enter a publication type.",
        unique=True,
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(800)],
    )

    def __str__(self):
        return self.name


class ArticleType(models.Model):
    name = models.CharField(
        max_length=STR_MED,
        help_text="Enter an article type.",
        unique=True,
    )
    weight = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )

    def __str__(self):
        return self.name


class Journal(models.Model):
    name = models.CharField(max_length=STR_LONGEST)
    full_name = models.CharField(max_length=STR_LONGEST)
    isi_listed = models.BooleanField(default=False)
    issn = models.CharField(max_length=STR_LONGEST, blank=True, null=True)
    eissn = models.CharField(max_length=STR_LONGEST, blank=True, null=True)
    impact_factor = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.full_name


class Publication(BaseModel):
    pub_type = models.ForeignKey(
        PublicationType,
        on_delete=models.PROTECT,
        verbose_name="Publication Type",
    )
    title = models.CharField(max_length=STR_LONGEST)
    chapter_title = models.CharField(
        "Chapter Title", max_length=STR_LONGEST, blank=True, null=True
    )
    authors = models.CharField(max_length=STR_LONGEST)
    chapter_authors = models.CharField(
        "Chapter Authors", max_length=STR_LONGEST, blank=True, null=True
    )
    publisher = models.CharField(max_length=STR_LONGEST, blank=True, null=True)
    city = models.CharField(max_length=STR_LONGEST, blank=True, null=True)
    isbn = models.CharField(
        "ISBN", max_length=STR_LONGEST, blank=True, null=True
    )
    article_type = models.ForeignKey(
        ArticleType,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Article Type",
    )
    journal = models.ForeignKey(
        Journal, on_delete=models.PROTECT, blank=True, null=True
    )
    other_journal_name = models.CharField(
        "Other Journal Name", max_length=STR_LONGEST, blank=True, null=True
    )
    volume = models.CharField(max_length=STR_LONGEST, blank=True, null=True)
    issue = models.CharField(max_length=STR_LONGEST, blank=True, null=True)
    start_page = models.CharField(
        max_length=STR_LONGEST, blank=True, null=True
    )
    end_page = models.CharField(max_length=STR_LONGEST, blank=True, null=True)
    pub_month = models.CharField(
        "Month", max_length=STR_LONGEST, blank=True, null=True
    )
    pub_year = models.CharField(
        "Year", max_length=STR_LONGEST, blank=True, null=True
    )
    pmid = models.CharField(
        "PMID", max_length=STR_LONGEST, blank=True, null=True
    )
    is_epub = models.BooleanField(default=False)
    conf_name = models.CharField(
        "Conference Name", max_length=STR_LONGEST, blank=True, null=True
    )
    conf_date = models.DateField("Conference Date", blank=True, null=True)
    ver_file = ContentTypeRestrictedFileField(
        "Verification File",
        upload_to="uploads/publications/",
        content_types=[
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "image/jpeg",
            "image/png",
        ],
        max_upload_size=2621440,
        blank=True,
        null=True,
    )
    ver_url = models.URLField("Verification URL", blank=True, null=True)

    def __str__(self):
        return self.title


class PublicationRole(models.Model):
    name = models.CharField(
        max_length=STR_MED,
        help_text="Enter a publication role.",
        unique=True,
    )
    weight = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(4)],
    )

    def __str__(self):
        return self.name


class PublicationLink(AdminMixin, CreatedUpdatedMixin):
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Author",
    )
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    role = models.ForeignKey(
        PublicationRole, on_delete=models.PROTECT, verbose_name="Author Role"
    )
    is_corresponding = models.BooleanField(
        "Corresponding Author", default=False
    )
    entry_type = None


class EditorialBoard(UserBaseModel):
    journal = models.ForeignKey(Journal, on_delete=models.PROTECT)
    other_journal_name = models.CharField(
        "Other Journal Name",
        max_length=STR_LONGEST,
        blank=True,
        help_text="Only required if 'Other' is selected from the Journal list.",
    )
    ver_file = ContentTypeRestrictedFileField(
        "Verification File",
        upload_to="uploads/editorial_boards/",
        content_types=[
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "image/jpeg",
            "image/png",
        ],
        max_upload_size=2621440,
        blank=True,
        null=True,
    )
    ver_url = models.URLField("Verification URL", blank=True, null=True)


class CommitteeWork(UserBaseModel):
    name = models.CharField(max_length=STR_LONG)
    hours = models.IntegerField()
    ver_file = ContentTypeRestrictedFileField(
        "Verification File",
        upload_to="uploads/committees/",
        content_types=[
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "image/jpeg",
            "image/png",
        ],
        max_upload_size=2621440,
        blank=True,
        null=True,
    )
    ver_url = models.URLField("Verification URL", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Committee work"

    def __str__(self):
        return self.name


class LectureType(models.Model):
    name = models.CharField(
        max_length=STR_LONG,
        help_text="Enter a lecture type.",
        unique=True,
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(150)],
    )

    def __str__(self):
        return self.name


class Lecture(UserBaseModel):
    lecture_type = models.ForeignKey(
        LectureType, on_delete=models.PROTECT, verbose_name="Lecture Type"
    )
    other_lecture_type = models.CharField(
        "Other Lecture Type", max_length=STR_MED, blank=True, null=True
    )
    name = models.CharField("Lecture Name", max_length=STR_LONGEST)
    course_code = models.CharField(
        "Course Name/Course Code", max_length=STR_MED, blank=True, null=True
    )
    start_date = models.DateField("Start Date")
    hours = models.DecimalField(
        "Hours (per lecture)", max_digits=5, decimal_places=2
    )
    is_cash = models.BooleanField(
        "Did you receive an honorarium for this lecture?", default=False
    )
    is_series = models.BooleanField(
        "Was this lecture part of a series?", default=False
    )
    end_date = models.DateField("End Date", blank=True, null=True)
    num_sessions = models.IntegerField("# Sessions", blank=True, null=True)
    ver_file = ContentTypeRestrictedFileField(
        "Verification File",
        upload_to="uploads/lectures/",
        content_types=[
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "image/jpeg",
            "image/png",
        ],
        max_upload_size=2621440,
        blank=True,
        null=True,
    )
    ver_url = models.URLField("Verification URL", blank=True, null=True)


class Student(models.Model):
    class StudentType(models.IntegerChoices):
        GRAD_STUDENT = 1, _("Graduate Student")
        RESEARCH_FELLOW = 2, _("Research Fellow")
        MED_STUDENT = 3, _("Medical Student")
        RESIDENT = 4, _("Resident")
        OTHER = 5, _("Other")

    class ResidentYear(models.IntegerChoices):
        PGY1 = 1, _("PGY-1")
        PGY2 = 2, _("PGY-2")
        PGY3 = 3, _("PGY-3")
        PGY4 = 4, _("PGY-4")
        PGY5 = 5, _("PGY-5")
        GRAD = 6, _("Graduated")

    first_name = models.CharField(
        _("first name"), max_length=STR_MED, blank=True
    )
    last_name = models.CharField(_("last name"), max_length=STR_MED)
    student_type = models.IntegerField(choices=StudentType.choices)
    other_student_type = models.CharField(max_length=STR_MED)
    resident_year = models.IntegerField(
        choices=ResidentYear.choices, blank=True, null=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ExamType(models.Model):
    name = models.CharField(
        max_length=STR_LONG,
        help_text="Enter an exam type.",
        unique=True,
    )
    weight = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(150)],
    )

    def __str__(self):
        return self.name


class Exam(UserBaseModel):
    exam_type = models.ForeignKey(
        ExamType, on_delete=models.PROTECT, verbose_name="Exam Type"
    )
    other_exam_name = models.CharField(
        "Other Exam Type",
        max_length=STR_MED,
        blank=True,
        null=True,
        help_text="Only required if 'Other' is selected from the Exam Type list.",
    )
    student_name = models.CharField(
        "Student Name",
        max_length=STR_MED,
        help_text="If multiple students, enter 'Various'.",
    )
    hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    date = models.DateField()
    ver_file = ContentTypeRestrictedFileField(
        "Verification File",
        upload_to="uploads/exams/",
        content_types=[
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "image/jpeg",
            "image/png",
        ],
        max_upload_size=2621440,
        blank=True,
        null=True,
    )
    ver_url = models.URLField("Verification URL", blank=True, null=True)


class SupervisionType(models.Model):
    name = models.CharField(max_length=STR_MED, unique=True)
    weight = models.IntegerField()

    def __str__(self):
        return self.name


class WorkFrequencyType(models.Model):
    name = models.CharField(
        max_length=STR_MED,
        unique=True,
    )
    days_equal = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        unique=True,
    )

    def __str__(self):
        return self.name


class Supervision(UserBaseModel):
    class ResidentYear(models.IntegerChoices):
        PGY1 = 1, _("PGY-1")
        PGY2 = 2, _("PGY-2")
        PGY3 = 3, _("PGY-3")
        PGY4 = 4, _("PGY-4")
        PGY5 = 5, _("PGY-5")
        GRAD = 6, _("Graduated")

    supervision_type = models.ForeignKey(
        SupervisionType,
        on_delete=models.PROTECT,
        verbose_name="Supervision Type",
    )
    student_name = models.CharField("Student Name", max_length=STR_MED)
    resident_year = models.IntegerField(
        choices=ResidentYear.choices, blank=True, null=True
    )
    duration = models.DecimalField(
        verbose_name="# of Months",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    frequency = models.ForeignKey(
        WorkFrequencyType, on_delete=models.PROTECT, blank=True, null=True
    )
    hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Only required for PAC attendance.",
    )
    ver_file = ContentTypeRestrictedFileField(
        "Verification File",
        upload_to="uploads/supervision/",
        content_types=[
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "image/jpeg",
            "image/png",
        ],
        max_upload_size=2621440,
        blank=True,
        null=True,
    )
    ver_url = models.URLField("Verification URL", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Supervision"


class Cpa(UserBaseModel):
    cpa_file = ContentTypeRestrictedFileField(
        "CPA File",
        upload_to="uploads/cpas/",
        content_types=[
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ],
        max_upload_size=2621440,
        blank=True,
        null=True,
    )
    ver_file = ContentTypeRestrictedFileField(
        "Verification File",
        upload_to="uploads/cpas/",
        content_types=[
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "image/jpeg",
            "image/png",
        ],
        max_upload_size=2621440,
        blank=True,
        null=True,
    )
    cpa_value = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(3000)]
    )
    entry_type = None

    class Meta:
        verbose_name = "CPA"
