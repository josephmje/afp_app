from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CreatedUpdatedMixin(models.Model):
    """
    This mixin provides fields for storing instance creation
    time and last update time.
    """

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    # created_user =
    modified_at = models.DateTimeField(auto_now=True)
    # modified_user =

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """On save, update timestamps."""
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(CreatedUpdatedMixin, self).save(*args, **kwargs)


class VerificationMixin(models.Model):
    """This mixin provides fields for"""

    ver_file = models.FileField("Verification file", blank=True, null=True)
    ver_url = models.URLField("Verification URL", blank=True, null=True)

    class Meta:
        abstract = True


class AdminMixin(models.Model):
    """
    This mixin provides fields for conveying the eligibility of
    a claim and reviewer decision comments.
    """

    class EntryType(models.IntegerChoices):
        SELF_REPORT = 1, _("Self-report")
        REGISTRY = 2, _("Data entered from registry")
        USER_EDIT = 3, _("Data entered and edited by physician")

    class EligibilityStatus(models.IntegerChoices):
        DOUBLE_CHECK = -2, _("To confirm")
        NOT_REVIEWED = -1, _("Not reviewed")
        INELIGIBLE = 0, _("Ineligible")
        ELIGIBLE = 1, _("Eligible")

    entry_type = models.IntegerField(choices=EntryType.choices, default=1)
    eligible = models.IntegerField(
        choices=EligibilityStatus.choices, default=-1
    )
    decision_comments = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
