from rest_framework.routers import DefaultRouter
from apps.core.views import (
    DataLookupTypeViewSet,
    DataLookupViewSet,
    SystemSettingViewSet
)

router = DefaultRouter()


router.register('datalookups', DataLookupViewSet, basename='datalookups')
router.register("lookup-types", DataLookupTypeViewSet, basename="lookup-types")
router.register(
    "system-settings", SystemSettingViewSet, basename="system-settings"
)

urlpatterns = router.urls
