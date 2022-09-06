import uuid

from afp_app.accounts.models import CustomUser, Rank
from afp_app.claims.mixins import (
    CreatedUpdatedMixin,
    EligibilityMixin,
    VerificationMixin,
)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField

STR_SHORT = 10
STR_MED = 50
STR_LONG = 100
STR_LONGEST = 255


class BaseModel(CreatedUpdatedMixin, VerificationMixin, EligibilityMixin):
    """Model representing a base class."""

    class EntryType(models.IntegerChoices):
        SELF_REPORT = 1, _("Self-report")
        REGISTRY = 2, _("Data entered from registry")
        USER_EDIT = 3, _("Data entered and edited by physician")

    comments = models.TextField(blank=True, null=True)
    entry_type = models.IntegerField(choices=EntryType.choices, default=1)

    class Meta:
        abstract = True


class UserBaseModel(BaseModel):
    uid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="Public identifier",
    )
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class AwardLevel(models.Model):
    """
    Model representing an award level (e.g. Local, Hospital,
    University, Provincial, National, International)
    and it's associated point value.
    """

    name = models.CharField(
        "Award Level",
        max_length=STR_MED,
        help_text="Enter an award level (e.g. Local, Hospital, etc.)",
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
        on_delete=models.PROTECT,
        related_name="award_level",
    )
    cash_prize = models.BooleanField(default=False)

    class Meta:
        ordering = ["award_level", "name"]

    def get_absolute_url(self):
        return reverse("award-detail", args=[str(self.id)])

    def __str__(self):
        return self.name

    @property
    def point_value(self):
        if self.cash_prize == True:
            return 0


class Promotion(UserBaseModel):
    promoted_to = models.ForeignKey(Rank, on_delete=models.PROTECT)


class GrantAgencyType(models.Model):
    name = models.CharField(
        max_length=STR_MED,
        help_text="Enter a grant agency type.",
    )

    def __str__(self):
        return self.name


class GrantCategory(models.Model):
    name = models.CharField(
        max_length=STR_MED,
        help_text="Enter a grant category.",
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
    name = models.CharField(max_length=STR_LONGEST)
    agency = models.ForeignKey(GrantAgency, on_delete=models.PROTECT)
    other_grant_agency = models.CharField(max_length=STR_MED)
    pi_list = models.CharField(max_length=STR_LONGEST)
    coi_list = models.CharField(max_length=STR_LONGEST)
    start_date = models.DateField()
    end_date = models.DateField()
    at_camh = models.BooleanField(default=False)


class GrantRole(models.Model):
    name = models.CharField(
        max_length=STR_MED,
        help_text="Enter a grant role.",
    )
    weight = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(7)],
    )

    def __str__(self):
        return self.name


class GrantLink(UserBaseModel):
    grant = models.ForeignKey(Grant, on_delete=models.CASCADE)
    role = models.ForeignKey(GrantRole, on_delete=models.PROTECT)


class GrantReviewType(models.Model):
    name = models.CharField(
        max_length=STR_MED,
        help_text="Enter a publication role.",
    )
    weight = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(2000)]
    )

    def __str__(self):
        return self.name


class GrantReview(UserBaseModel):
    type = models.ForeignKey(GrantReviewType, on_delete=models.PROTECT)
    agency = models.CharField(max_length=STR_LONG)
    name = models.CharField(max_length=STR_LONG)
    date = models.DateField()
    is_member = models.BooleanField(default=False)
    num_days = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(25)],
    )


class PublicationType(models.Model):
    name = models.CharField(
        max_length=STR_MED,
        help_text="Enter a publication type.",
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


class Publication(BaseModel):
    pub_type = models.ForeignKey(PublicationType, on_delete=models.PROTECT)
    authors = models.CharField(max_length=STR_LONGEST)
    title = models.CharField(max_length=STR_LONGEST)
    publisher = models.CharField(max_length=STR_LONGEST, blank=True, null=True)
    isbn = models.CharField(max_length=STR_LONGEST, blank=True, null=True)
    article_type = models.ForeignKey(
        ArticleType, on_delete=models.PROTECT, blank=True, null=True
    )
    journal = models.ForeignKey(
        Journal, on_delete=models.PROTECT, blank=True, null=True
    )
    other_journal_name = models.CharField(
        max_length=STR_LONGEST, blank=True, null=True
    )
    volume = models.CharField(max_length=STR_LONGEST, blank=True, null=True)
    issue = models.CharField(max_length=STR_LONGEST, blank=True, null=True)
    start_page = models.CharField(
        max_length=STR_LONGEST, blank=True, null=True
    )
    end_page = models.CharField(max_length=STR_LONGEST, blank=True, null=True)
    pub_month = models.CharField(max_length=STR_LONGEST, blank=True, null=True)
    pub_year = models.CharField(max_length=STR_LONGEST, blank=True, null=True)
    pmid = models.CharField(max_length=STR_LONGEST, blank=True, null=True)
    other_impact_factor = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )
    is_epub = models.BooleanField(default=False)
    conf_name = models.CharField(max_length=STR_LONGEST, blank=True, null=True)
    location = models.CharField(max_length=STR_LONGEST, blank=True, null=True)


class PublicationRole(models.Model):
    name = models.CharField(
        max_length=STR_MED,
        help_text="Enter a publication role.",
    )
    weight = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(4)],
    )

    def __str__(self):
        return self.name


class PublicationLink(UserBaseModel):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    role = models.ForeignKey(PublicationRole, on_delete=models.PROTECT)


class EditorialBoard(UserBaseModel):
    journal = models.ForeignKey(Journal, on_delete=models.PROTECT)
    other_journal_name = models.CharField(
        max_length=STR_LONGEST, blank=True, null=True
    )


class CommitteeWork(UserBaseModel):
    name = models.CharField(max_length=STR_LONG)
    hours = models.IntegerField()


class LectureType(models.Model):
    name = models.CharField(
        max_length=STR_LONG,
        help_text="Enter a lecture type.",
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(150)],
    )

    def __str__(self):
        return self.name


class Lecture(UserBaseModel):
    lecture_type = models.ForeignKey(LectureType, on_delete=models.PROTECT)
    other_lecture_type = models.CharField(
        max_length=STR_MED, blank=True, null=True
    )
    name = models.CharField(max_length=STR_LONGEST)
    course_code = models.CharField(max_length=STR_MED, blank=True, null=True)
    start_date = models.DateField()
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    is_cash = models.BooleanField(default=False)
    is_series = models.BooleanField(default=False)
    end_date = models.DateField(blank=True, null=True)
    num_sessions = models.IntegerField()


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

    first_name = models.CharField(_("first name"), max_length=STR_MED)
    last_name = models.CharField(_("last name"), max_length=STR_MED)
    student_type = models.IntegerField(choices=StudentType.choices)
    other_student_type = models.CharField(max_length=STR_MED)
    resident_year = models.IntegerField(
        choices=ResidentYear.choices, blank=True, null=True
    )


class ExamType(models.Model):
    name = models.CharField(
        max_length=STR_LONG,
        help_text="Enter an exam type.",
    )
    weight = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(150)],
    )

    def __str__(self):
        return self.name


class Exam(UserBaseModel):
    exam_type = models.ForeignKey(ExamType, on_delete=models.PROTECT)
    other_exam_name = models.CharField(
        max_length=STR_MED, blank=True, null=True
    )
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    date = models.DateField()


class SupervisionType(models.Model):
    name = models.CharField(max_length=STR_MED)
    weight = models.IntegerField()

    def __str__(self):
        return self.name


class WorkFrequencyType(models.Model):
    name = models.CharField(max_length=STR_MED)
    days_equal = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )


class Supervision(UserBaseModel):
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT)
    supervision_type = models.ForeignKey(
        SupervisionType, on_delete=models.PROTECT
    )
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    duration = models.DecimalField(max_digits=5, decimal_places=2)
    med_duration = models.DecimalField(max_digits=5, decimal_places=2)
    frequency = models.ForeignKey(WorkFrequencyType, on_delete=models.PROTECT)
