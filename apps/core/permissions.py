from django.apps import apps
from rest_access_policy import AccessPolicy


class AbstractAccessPolicy(AccessPolicy):
    group_prefix = "role:"

    @classmethod
    def load_policies(cls):
        """Retrieve policies from the preloaded AppConfig."""
        policies = apps.get_app_config("core").policies
        return policies.get(cls.__name__, {})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.statements = self.load_policies().get("statements", [])

    def get_user_group_values(self, user):
        """Return the user's role code if authenticated; otherwise, return an empty list."""
        return (
            [getattr(user.role, "code", None)]
            if getattr(user, "is_authenticated", False) and getattr(user, "role", None)
            else []
        )


class DataLookupAccessPolicy(AbstractAccessPolicy):
    @classmethod
    def scope_queryset(cls, request, queryset):
        return queryset


class SystemSettingAccessPolicy(AbstractAccessPolicy):
    @classmethod
    def scope_queryset(cls, request, queryset):
        return queryset
