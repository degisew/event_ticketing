import logging
from django.core.cache import cache
from apps.core.models import DataLookup
from apps.core.exceptions import DataIntegrityError

logger = logging.getLogger(__name__)


class DataLookupService:
    @staticmethod
    def get_cached_lookup(type: str, value: str):
        if not type or not value:
            # TODO: This should have proper vustom exception.
            raise ValueError("Invalid lookup type or value")
        key: str = f"lookup_{type}_{value}"

        result = cache.get(key)

        if not result:
            try:
                result = DataLookup.objects.get(type=type, value=value)

                cache.set(key, result, timeout=3600)
            except DataLookup.DoesNotExist:
                raise DataIntegrityError(
                    detail={
                        "System configuration error: Required DataLookup not found."
                    }
                )
        return result
