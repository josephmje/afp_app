from django.contrib import admin
from django.utils.html import format_html
from django import forms

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
admin.site.register(GrantLink)
admin.site.register(GrantRole)
admin.site.register(LectureType)
admin.site.register(Promotion)
admin.site.register(PublicationLink)
admin.site.register(PublicationType)
admin.site.register(PublicationRole)
admin.site.register(SupervisionType)
admin.site.register(WorkFrequencyType)


admin.site.register(Journal)


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
        "name",
        "organization",
        "award_level",
        "cash_prize",
        "comments",
        "ver_file",
        "ver_url",
        "entry_type",
        "status",
        "decision_comments",
    ]
    list_filter = ["eligible", "award_level"]

    def status(self, obj):
        if obj.eligible == -2:
            color = "yellow"
        elif obj.eligible == 0:
            color = "red"
        elif obj.eligible == 1:
            color = "green"
        else:
            color = "grey"
        return format_html(
            f'<strong><p style="color: {color}">{obj.eligible}</p></strong>'
        )

    status.allow_tags = True

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


class PublicationLinkInLineAdmin(admin.TabularInline):
    model = PublicationLink
    extra = 1
    list_display = [
        "user_id",
        "role",
        "eligible",
        "decision_comments",
    ]
    fieldsets = (
        (
            None,
            {"fields": (("user_id", "role"),)},
        ),
        ("Admin", {"fields": ("eligible", "decision_comments")}),
    )


class PublicationAdmin(admin.ModelAdmin):
    list_display = [
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
        "entry_type",
        "eligible",
        "decision_comments",
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


admin.site.register(Publication, PublicationAdmin)


@admin.register(EditorialBoard)
class EditorialBoardAdmin(admin.ModelAdmin):

    list_display = [
        "user_id",
        "journal",
        "other_journal_name",
        "comments",
        "ver_file",
        "ver_url",
        "entry_type",
        "eligible",
        "decision_comments",
    ]
    list_filter = ["eligible"]

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


class GrantLinkInLineAdmin(admin.TabularInline):
    model = GrantLink
    extra = 1
    list_display = [
        "user_id",
        "role",
        "eligible",
        "decision_comments",
    ]
    fieldsets = (
        (
            None,
            {"fields": (("user_id", "role"),)},
        ),
        ("Admin", {"fields": ("eligible", "decision_comments")}),
    )


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
        "at_camh",
        "comments",
        "ver_file",
        "ver_url",
        "entry_type",
        "eligible",
        "decision_comments",
    ]
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


admin.site.register(Grant, GrantAdmin)


@admin.register(GrantReview)
class GrantReviewAdmin(admin.ModelAdmin):

    list_display = [
        "user_id",
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
        "entry_type",
        "eligible",
        "decision_comments",
    ]
    list_filter = ["eligible"]

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
        "name",
        "hours",
        "comments",
        "ver_file",
        "ver_url",
        "entry_type",
        "eligible",
        "decision_comments",
    ]
    list_filter = ["eligible"]

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
        "entry_type",
        "eligible",
        "decision_comments",
    ]
    list_filter = ["eligible"]

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


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):

    list_display = [
        "user_id",
        "exam_type",
        "other_exam_name",
        "student",
        "other_student_name",
        "date",
        "hours",
        "comments",
        "ver_file",
        "ver_url",
        "entry_type",
        "eligible",
        "decision_comments",
    ]
    list_filter = ["eligible"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user_id",
                    ("exam_type", "other_exam_name"),
                    ("student", "other_student_name"),
                    ("date", "hours"),
                    "comments",
                    ("ver_file", "ver_url"),
                )
            },
        ),
        ("Admin", {"fields": ("entry_type", "eligible", "decision_comments")}),
    )


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
        "supervision_type",
        "student_id",
        "other_student_name",
        "hours",
        "duration",
        "frequency",
        "comments",
        "ver_file",
        "ver_url",
        "entry_type",
        "eligible",
        "decision_comments",
    ]
    list_filter = ["eligible"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user_id",
                    "supervision_type",
                    ("student_id", "other_student_name"),
                    ("hours", "duration", "frequency"),
                    "comments",
                    ("ver_file", "ver_url"),
                )
            },
        ),
        ("Admin", {"fields": ("entry_type", "eligible", "decision_comments")}),
    )


@admin.register(Cpa)
class CpaAdmin(admin.ModelAdmin):

    list_display = [
        "user_id",
        "cpa_file",
        "ver_file",
        "comments",
        "eligible",
        "decision_comments",
    ]
    list_filter = ["eligible"]

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
