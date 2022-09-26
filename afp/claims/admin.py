from django.contrib import admin

from .models import (
    ArticleType,
    Award,
    AwardLevel,
    CommitteeWork,
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
admin.site.register(CommitteeWork)
admin.site.register(EditorialBoard)
admin.site.register(Exam)
admin.site.register(ExamType)
admin.site.register(Grant)
admin.site.register(GrantAgency)
admin.site.register(GrantAgencyType)
admin.site.register(GrantCategory)
admin.site.register(GrantLink)
admin.site.register(GrantReview)
admin.site.register(GrantReviewType)
admin.site.register(GrantRole)
admin.site.register(Journal)
admin.site.register(Lecture)
admin.site.register(LectureType)
admin.site.register(Promotion)
admin.site.register(Publication)
admin.site.register(PublicationLink)
admin.site.register(PublicationType)
admin.site.register(PublicationRole)
admin.site.register(Student)
admin.site.register(Supervision)
admin.site.register(SupervisionType)
admin.site.register(WorkFrequencyType)


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    """Administration object for Award models.
    Defines:
     - fields to be displayed in list view (list_display)
     - filters that will be displayed in sidebar (list_filter)
     - grouping of fields into sections (fieldsets)
    """

    list_display = (
        "user_id",
        "name",
        "organization",
        "award_level",
        "cash_prize",
        "comments",
        "ver_file",
        "ver_url",
        "entry_type",
        "eligible",
        "decision_comments",
    )
    list_filter = ["award_level"]

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
