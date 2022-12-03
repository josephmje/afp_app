from django import forms
from django.db import models
from django.template.defaultfilters import filesizeformat
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CreatedUpdatedMixin(models.Model):
    """
    This mixin provides fields for storing instance creation
    time and last update time.
    """

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """On save, update timestamps."""
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(CreatedUpdatedMixin, self).save(*args, **kwargs)


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


def user_directory_path(instance, filename):
    return f"uploads/{instance.user_id}/{instance._meta.model._meta.verbose_name.title()}/{filename}"


class VerificationMixin(models.Model):

    ver_file = ContentTypeRestrictedFileField(
        "Verification File",
        upload_to=user_directory_path,
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
