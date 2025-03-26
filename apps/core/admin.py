from django.contrib import admin
from environ import Env
from django.utils.translation import gettext_lazy as _

from apps.core.models import DataLookup, SystemSetting

env = Env()


@admin.register(DataLookup)
class DataLookupAdmin(admin.ModelAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "type",
                    "name",
                    "value",
                    "category",
                    "is_default",
                    "note",
                    "index",
                ),
            },
        ),
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "type",
                    "name",
                    "description",
                    "value",
                    "category",
                    "is_default",
                    "note",
                    "index",
                )
            },
        ),
        (
            _("Actions"),
            {
                "classes": ("collapse",),
                "fields": (
                    "remark",
                ),
            },
        ),
    )

    list_display = (
        "type",
        "name",
        "value",
        "category",
        "is_default",
        "index",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "updated_at",
        "type",
        "category",
    )


admin.site.register(SystemSetting)


admin.site.site_title = _(env("APP_TITLE", cast=str))
admin.site.site_header = _(env("APP_TITLE", cast=str))
admin.site.index_title = _(env("INDEX_TITLE", cast=str))