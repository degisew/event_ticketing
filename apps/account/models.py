from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.account.managers import UserManager
from apps.core.models import AbstractBaseModel, DataLookup


class Role(AbstractBaseModel):
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    code = models.CharField(max_length=50, verbose_name=_("Code"))

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")
        db_table = "roles"
        constraints = [
            models.UniqueConstraint(fields=["code"], name="roles_code_idx"),
        ]

    def __str__(self) -> str:
        return self.name


class User(AbstractUser, AbstractBaseModel):
    email = models.EmailField(verbose_name=_("email address"), unique=True)

    role = models.ForeignKey(
        Role, null=True, blank=True, on_delete=models.RESTRICT, related_name="+"
    )

    is_profile_set = models.BooleanField(default=True)

    state = models.ForeignKey(
        DataLookup,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="+",
        limit_choices_to={"type": "account_state_type"},
    )

    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("-created_at",)
        db_table = "users"

    def __str__(self) -> str:
        return self.email


class UserPreferences(AbstractBaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name="preferences",
        related_query_name="preference",
    )

    notification_enabled = models.BooleanField(
        default=True, verbose_name=_("Notification Enabled")
    )

    class Meta:
        verbose_name = _("User Preference")
        verbose_name_plural = _("User Preferences")
        ordering = ("-created_at",)
        db_table = "user_preferences"

    def __str__(self):
        return self.user.email


class UserProfile(AbstractBaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    first_name = models.CharField(verbose_name=_("First Name"), max_length=100)

    last_name = models.CharField(verbose_name=_("Last Name"), max_length=100)

    phone = models.CharField(
        verbose_name=_("Phone Number"), max_length=15, blank=True, null=True
    )

    avatar = models.ImageField(
        verbose_name=_("Avatar"),
        upload_to="mediafiles/user_profiles/",
        blank=True,
        null=True,
    )

    address = models.TextField(verbose_name=_("Address"), blank=True, null=True)

    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")
        ordering = ("-created_at",)
        db_table = "user_profiles"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
