from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

STR_SHORT = 10
STR_MED = 50
STR_LONG = 100
STR_LONGEST = 255


class CustomUserManager(UserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with a given email and password.
        """
        if not email:
            raise ValueError(_("User must have an email address."))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, username):
        case_insensitive_username_field = (
            f"{self.model.USERNAME_FIELD}__iexact"
        )
        return self.get(**{case_insensitive_username_field: username})


class Division(models.Model):
    """Model representing a user's clinical division."""

    name = models.CharField(
        "Clinical Division",
        max_length=STR_MED,
        help_text="Enter clinical division.",
    )

    def __str__(self):
        return self.name


class Rank(models.Model):
    """Model representing a user's academic rank."""

    name = models.CharField(
        "Rank",
        max_length=STR_MED,
        help_text="Enter academic rank.",
    )

    def __str__(self):
        return self.name


class UserManagerActive(models.Manager):
    def get_queryset(self):
        return (
            super(UserManagerActive, self)
            .get_queryset()
            .filter(is_active=True)
        )


class CustomUser(AbstractUser):
    """Model extending Django's `AbstractUser` class."""

    first_name = models.CharField(_("first name"), max_length=STR_MED)
    middle_name = models.CharField(
        _("middle name"), max_length=STR_MED, blank=True, null=True
    )
    last_name = models.CharField(_("last name"), max_length=STR_MED)
    email = models.EmailField(_("email address"), unique=True)
    is_physician = models.BooleanField(default=True)
    is_scientist = models.BooleanField(default=False)
    division = models.ForeignKey(
        "division", on_delete=models.SET_NULL, null=True
    )
    other_division = models.CharField(
        max_length=STR_MED, blank=True, null=True
    )
    rank = models.ForeignKey("rank", on_delete=models.SET_NULL, null=True)
    archived_at = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    active = UserManagerActive()

    class Meta:
        ordering = ["first_name", "last_name"]

    @classmethod
    def count_all(
        cls,
    ):
        return cls.objects.filter(is_active=True).count()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Physician(models.Model):
    """Model extending `CustomUser` class with unique fields for physicians."""

    user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    class ProtectedTime(models.IntegerChoices):
        NO = 0, _("No")
        YES = 1, _("Yes")
        UNKNOWN = 2, _("Unknown")

    fte = models.DecimalField(
        "FTE",
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        blank=True,
        null=True,
    )
    protected_time = models.IntegerField(choices=ProtectedTime.choices)
