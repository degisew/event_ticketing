from apps.core.permissions import AbstractAccessPolicy


class UserAccessPolicy(AbstractAccessPolicy):
    @classmethod
    def scope_queryset(cls, request, queryset):
        return queryset


class CompanyProfileAccessPolicy(AbstractAccessPolicy):
    @classmethod
    def scope_queryset(cls, request, queryset):
        return queryset.filter(user=request.user)


class RoleAccessPolicy(AbstractAccessPolicy):
    @classmethod
    def scope_queryset(cls, request, queryset):
        return queryset
