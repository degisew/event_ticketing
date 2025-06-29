from uuid import UUID
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from apps.account.models import Role


class RoleService:
    @staticmethod
    def get_cached_role(id: UUID):
        key = f"role_{id}"

        result = cache.get(key)

        if not result:
            result = get_object_or_404(Role, id=id)
            cache.set(key, result, timeout=3600)

        return result
