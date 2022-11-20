from django.contrib import admin
from django.utils.html import format_html

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
admin.site.register(CommitteeWork)
admin.site.register(Cpa)
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


class PublicationAdmin(admin.ModelAdmin):
    inlines = [PublicationLinkInLineAdmin]


admin.site.register(Publication, PublicationAdmin)
