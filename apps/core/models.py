import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractBaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("id"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated at"),
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("deleted at"),
    )

    class Meta:
        abstract = True


class DataLookup(AbstractBaseModel):
    type = models.CharField(max_length=200, verbose_name=_("Type"))

    name = models.CharField(max_length=200, verbose_name=_("Name"))

    value = models.CharField(unique=True, max_length=200, verbose_name=_("Value"))

    description = models.TextField(blank=True, verbose_name=_("Description"))

    category = models.CharField(max_length=200, blank=True, verbose_name=_("Category"))

    note = models.TextField(blank=True, verbose_name=_("Note"))

    index = models.PositiveIntegerField(default=0, verbose_name=_("Index"))

    is_default = models.BooleanField(default=False, verbose_name=_("Is Default"))

    is_active = models.BooleanField(default=False, verbose_name=_("Is Active"))

    remark = models.TextField(blank=True, verbose_name=_("Remark"))

    data_type = models.CharField(max_length=200, verbose_name=_("Data Type"))

    class Meta:
        verbose_name = _("Data Lookup")
        verbose_name_plural = _("Data Lookups")
        db_table = "data_lookups"
        constraints = [
            # Constraint: Only one default value per type
            models.UniqueConstraint(
                fields=["type", "is_default"],
                condition=models.Q(is_default=True),
                name="data_lookups_type_is_default_idx",
            ),
            # Constraint: Unique index for each type
            models.UniqueConstraint(
                fields=["type", "index"], name="data_lookups_type_index_idx"
            ),
            # Constraint: Unique value across all types
            models.UniqueConstraint(fields=["value"], name="data_lookups_value_idx"),
        ]

    def __str__(self):
        return f"{self.type} :: {self.name}"


class SystemSetting(AbstractBaseModel):
    name = models.CharField(max_length=200, verbose_name=_("Name"))

    key = models.CharField(max_length=200, verbose_name=_("Key"))

    default_value = models.CharField(max_length=256, verbose_name=_("default_value"))

    current_value = models.CharField(max_length=256, verbose_name=_("current_value"))

    data_type = models.ForeignKey(
        DataLookup,
        on_delete=models.RESTRICT,
        related_name="+",
        blank=True,
        null=True,
        limit_choices_to={"type": "data_type"},
    )

    class Meta:
        verbose_name = _("System Setting")
        verbose_name_plural = _("System Settings")
        db_table = "system_settings"
        constraints = [
            models.UniqueConstraint(
                fields=["key"],
                condition=models.Q(deleted_at__isnull=True),
                name="system_settings_key_idx",
            ),
        ]

    def __str__(self):
        return f"{self.name} :: {self.current_value}"
