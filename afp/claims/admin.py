from django import forms
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse

from .models import (
    ArticleType,
    Award,
    AwardLevel,
    CommitteeWork,
    Cpa,
    EditorialBoard,
    Exam,
    ExamType,
    Grant,
    GrantAgency,
    GrantAgencyType,
    GrantCategory,
    GrantLink,
    GrantReview,
    GrantReviewType,
    GrantRole,
    Journal,
    Lecture,
    LectureType,
    Promotion,
    Publication,
    PublicationLink,
    PublicationRole,
    PublicationType,
    Student,
    Supervision,
    SupervisionType,
    WorkFrequencyType,
)

admin.site.register(ArticleType)
admin.site.register(AwardLevel)
admin.site.register(ExamType)
admin.site.register(GrantAgency)
admin.site.register(GrantAgencyType)
admin.site.register(GrantCategory)
admin.site.register(GrantReviewType)
admin.site.register(GrantRole)
admin.site.register(LectureType)
admin.site.register(PublicationType)
admin.site.register(PublicationRole)
admin.site.register(SupervisionType)
admin.site.register(WorkFrequencyType)


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    """Administration object for Award models.
    Defines:
     - fields to be displayed in list view (list_display)
     - filters that will be displayed in sidebar (list_filter)
     - grouping of fields into sections (fieldsets)
    """

    list_display = [
        "user_id",
        "eligible",
        "name",
        "organization",
        "cash_prize",
        "comments",
        "ver_file",
        "ver_url",
        "decision_comments",
    ]
    list_filter = ["eligible", "award_level"]
    list_editable = ["eligible", "decision_comments"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user_id",
                    "name",
                    "organization",
                    "award_level",
                    "cash_prize",
                    "comments",
                    ("ver_file", "ver_url"),
                )
            },
        ),
        ("Admin", {"fields": ("entry_type", "eligible", "decision_comments")}),
    )


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):

    list_display = [
        "user_id",
        "eligible",
        "promoted_to",
        "comments",
        "ver_file",
        "ver_url",
        "decision_comments",
    ]
    list_filter = ["eligible", "promoted_to"]
    list_editable = ["eligible", "decision_comments"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user_id",
                    "promoted_to",
                    "comments",
                    ("ver_file", "ver_url"),
                )
            },
        ),
        ("Admin", {"fields": ("entry_type", "eligible", "decision_comments")}),
    )


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("upload_csv/", self.upload_csv),
        ]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith(".csv"):
                messages.warning(request, "The wrong file type was uploaded")
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data:
                fields = x.split(",")
                created = Journal.objects.update_or_create(
                    id=fields[0],
                    name=fields[1],
                    full_name=fields[2],
                    issn=fields[3],
                    eissn=fields[4],
                    impact_factor=fields[5],
                    isi_listed=fields[6].rstrip(),
                )
            url = reverse("admin:index")
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/claims/csv_upload.html", data)


@admin.register(PublicationLink)
class PublicationLinkAdmin(admin.ModelAdmin):

    list_display = [
        "publication",
        "eligible",
        "user_id",
        "role",
        "decision_comments",
    ]
    list_filter = ["eligible"]
    list_editable = ["eligible", "decision_comments"]


class PublicationLinkInLineAdmin(admin.TabularInline):
    model = PublicationLink
    extra = 1
    list_display = [
        "user_id",
        "role",
        "is_corresponding",
        "eligible",
        "decision_comments",
    ]
    fieldsets = (
        (
            None,
            {"fields": (("user_id", "role", "is_corresponding"),)},
        ),
        ("Admin", {"fields": ("eligible", "decision_comments")}),
    )


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "eligible",
        "authors",
        "volume",
        "issue",
        "start_page",
        "end_page",
        "pub_month",
        "pub_year",
        "pmid",
        "is_epub",
        "ver_url",
        "decision_comments",
    ]
    list_editable = [
        "is_epub",
        "eligible",
        "decision_comments",
    ]
    list_filter = [
        "entry_type",
        "eligible",
        "pub_type",
        "article_type",
        "is_epub",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "pub_type",
                    ("title", "chapter_title"),
                    ("authors", "chapter_authors"),
                    ("publisher", "city", "isbn"),
                    "article_type",
                    ("journal", "other_journal_name"),
                    ("volume", "issue", "start_page", "end_page"),
                    ("pub_month", "pub_year", "pmid", "is_epub"),
                    ("conf_name", "conf_date"),
                    "comments",
                    ("ver_file", "ver_url"),
                )
            },
        ),
        ("Admin", {"fields": ("entry_type", "eligible", "decision_comments")}),
    )
    inlines = [PublicationLinkInLineAdmin]

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("upload_csv/", self.upload_csv),
        ]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith(".csv"):
                messages.warning(request, "The wrong file type was uploaded")
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data:
                fields = x.split(",")
                created = Publication.objects.update_or_create(
                    pmid=fields[0],
                    pub_type_id=fields[1],
                    title=fields[2],
                    authors=fields[3],
                    article_type_id=fields[4],
                    journal_id=fields[5],
                    other_journal_name=fields[6],
                    volume=fields[7],
                    issue=fields[8],
                    start_page=fields[9],
                    end_page=fields[10],
                    pub_year=fields[11],
                    pub_month=fields[12],
                    is_epub=fields[13],
                    ver_url=fields[14],
                    entry_type=fields[15].rstrip(),
                )
            url = reverse("admin:index")
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/claims/csv_upload.html", data)


@admin.register(EditorialBoard)
class EditorialBoardAdmin(admin.ModelAdmin):

    list_display = [
        "user_id",
        "eligible",
        "journal",
        "other_journal_name",
        "comments",
        "ver_file",
        "ver_url",
        "decision_comments",
    ]
    list_filter = ["eligible"]
    list_editable = ["eligible", "decision_comments"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user_id",
                    "journal",
                    "other_journal_name",
                    "comments",
                    ("ver_file", "ver_url"),
                )
            },
        ),
        ("Admin", {"fields": ("entry_type", "eligible", "decision_comments")}),
    )


@admin.register(GrantLink)
class GrantLinkAdmin(admin.ModelAdmin):

    list_display = [
        "grant",
        "eligible",
        "user_id",
        "role",
        "decision_comments",
    ]
    list_filter = ["eligible"]
    list_editable = ["eligible", "decision_comments"]


class GrantLinkInLineAdmin(admin.TabularInline):
    model = GrantLink
    extra = 1
    list_display = [
        "user_id",
        "eligible",
        "role",
        "decision_comments",
    ]
    fieldsets = (
        (
            None,
            {"fields": (("user_id", "role"),)},
        ),
        ("Admin", {"fields": ("eligible", "decision_comments")}),
    )


@admin.register(Grant)
class GrantAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "pi_list",
        "coi_list",
        "agency",
        "other_grant_agency",
        "amount",
        "start_date",
        "end_date",
        "comments",
        "ver_file",
        "ver_url",
        "eligible",
        "decision_comments",
    ]
    list_filter = ["eligible", "at_camh"]
    list_editable = ["eligible", "decision_comments"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    ("pi_list", "coi_list"),
                    ("agency", "other_grant_agency"),
                    ("amount", "start_date", "end_date"),
                    "at_camh",
                    "comments",
                    ("ver_file", "ver_url"),
                )
            },
        ),
        ("Admin", {"fields": ("entry_type", "eligible", "decision_comments")}),
    )
    inlines = [GrantLinkInLineAdmin]

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("upload_csv/", self.upload_csv),
        ]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith(".csv"):
                messages.warning(request, "The wrong file type was uploaded")
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data:
                fields = x.split(",")
                created = Grant.objects.update_or_create(
                    amount=fields[0],
                    name=fields[1],
                    pi_list=fields[2],
                    coi_list=fields[3],
                    at_camh=fields[4],
                    agency_id=fields[5],
                    other_grant_agency=fields[6],
                    start_date=fields[7],
                    end_date=fields[8].rstrip(),
                )
            url = reverse("admin:index")
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/claims/csv_upload.html", data)


@admin.register(GrantReview)
class GrantReviewAdmin(admin.ModelAdmin):

    list_display = [
        "user_id",
        "eligible",
        "type",
        "agency",
        "date",
        "name",
        "is_member",
        "num_days",
        "num_reviewed",
        "comments",
        "ver_file",
        "ver_url",
        "decision_comments",
    ]
    list_filter = ["entry_type", "eligible", "type"]
    list_editable = ["eligible", "decision_comments"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user_id",
                    "type",
                    "agency",
                    "date",
                    "name",
                    "is_member",
                    "num_days",
                    "num_reviewed",
                    "comments",
                    ("ver_file", "ver_url"),
                )
            },
        ),
        ("Admin", {"fields": ("entry_type", "eligible", "decision_comments")}),
    )


@admin.register(CommitteeWork)
class CommitteeWorkAdmin(admin.ModelAdmin):

    list_display = [
        "user_id",
        "eligible",
        "name",
        "hours",
        "comments",
        "ver_file",
        "ver_url",
        "decision_comments",
    ]
    list_filter = ["entry_type", "eligible"]
    list_editable = ["eligible", "decision_comments"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user_id",
                    "name",
                    "hours",
                    "comments",
                    ("ver_file", "ver_url"),
                )
            },
        ),
        ("Admin", {"fields": ("entry_type", "eligible", "decision_comments")}),
    )


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):

    list_display = [
        "user_id",
        "eligible",
        "lecture_type",
        "other_lecture_type",
        "name",
        "course_code",
        "start_date",
        "hours",
        "end_date",
        "num_sessions",
        "comments",
        "ver_file",
        "ver_url",
        "decision_comments",
    ]
    list_filter = ["entry_type", "eligible", "lecture_type", "is_cash"]
    list_editable = ["eligible", "decision_comments"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user_id",
                    ("lecture_type", "other_lecture_type"),
                    ("name", "course_code"),
                    ("start_date", "hours"),
                    "is_cash",
                    ("is_series", "end_date", "num_sessions"),
                    "comments",
                    ("ver_file", "ver_url"),
                )
            },
        ),
        ("Admin", {"fields": ("entry_type", "eligible", "decision_comments")}),
    )

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("upload_csv/", self.upload_csv),
        ]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith(".csv"):
                messages.warning(request, "The wrong file type was uploaded")
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data:
                fields = x.split(",")
                created = Lecture.objects.update_or_create(
                    user_id_id=fields[0],
                    lecture_type_id=fields[1],
                    name=fields[2],
                    course_code=fields[3],
                    start_date=fields[4],
                    hours=fields[5],
                    is_series=fields[6],
                    num_sessions=fields[7],
                    end_date=fields[8],
                    eligible=fields[9],
                    entry_type=fields[10],
                )
            url = reverse("admin:index")
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/claims/csv_upload.html", data)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):

    list_display = [
        "user_id",
        "eligible",
        "exam_type",
        "other_exam_name",
        "student_name",
        "date",
        "hours",
        "comments",
        "ver_file",
        "ver_url",
        "decision_comments",
    ]
    list_filter = ["entry_type", "eligible", "exam_type"]
    list_editable = ["eligible", "decision_comments"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user_id",
                    ("exam_type", "other_exam_name"),
                    ("student_name"),
                    ("date", "hours"),
                    "comments",
                    ("ver_file", "ver_url"),
                )
            },
        ),
        ("Admin", {"fields": ("entry_type", "eligible", "decision_comments")}),
    )

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("upload_csv/", self.upload_csv),
        ]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith(".csv"):
                messages.warning(request, "The wrong file type was uploaded")
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data:
                fields = x.split(",")
                created = Exam.objects.update_or_create(
                    user_id_id=fields[0],
                    exam_type_id=fields[1],
                    student_name=fields[2],
                    date=fields[3],
                    hours=fields[4],
                    eligible=fields[5],
                    entry_type=fields[6],
                )
            url = reverse("admin:index")
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/claims/csv_upload.html", data)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = [
        "first_name",
        "last_name",
        "student_type",
        "other_student_type",
        "resident_year",
    ]
    list_filter = ["student_type"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("first_name", "last_name"),
                    ("student_type", "other_student_type"),
                    "resident_year",
                )
            },
        ),
    )


@admin.register(Supervision)
class SupervisionAdmin(admin.ModelAdmin):

    list_display = [
        "user_id",
        "eligible",
        "supervision_type",
        "student_name",
        "hours",
        "duration",
        "frequency",
        "comments",
        "ver_file",
        "ver_url",
        "decision_comments",
    ]
    list_filter = ["entry_type", "eligible", "supervision_type"]
    list_editable = ["eligible", "decision_comments"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user_id",
                    "supervision_type",
                    ("student_name", "resident_year"),
                    ("hours", "duration", "frequency"),
                    "comments",
                    ("ver_file", "ver_url"),
                )
            },
        ),
        ("Admin", {"fields": ("entry_type", "eligible", "decision_comments")}),
    )

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("upload_csv/", self.upload_csv),
        ]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith(".csv"):
                messages.warning(request, "The wrong file type was uploaded")
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data:
                fields = x.split(",")
                created = Supervision.objects.update_or_create(
                    user_id_id=fields[0],
                    supervision_type_id=fields[1],
                    student_name=fields[2],
                    duration=fields[3],
                    frequency_id=fields[4],
                    eligible=fields[5],
                    entry_type=fields[6],
                )
            url = reverse("admin:index")
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/claims/csv_upload.html", data)


@admin.register(Cpa)
class CpaAdmin(admin.ModelAdmin):

    list_display = [
        "user_id",
        "eligible",
        "cpa_file",
        "ver_file",
        "comments",
        "decision_comments",
    ]
    list_filter = ["eligible"]
    list_editable = ["eligible", "decision_comments"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user_id",
                    ("cpa_file", "ver_file"),
                    "comments",
                )
            },
        ),
        ("Admin", {"fields": ("eligible", "decision_comments")}),
    )
