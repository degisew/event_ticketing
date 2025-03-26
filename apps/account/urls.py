from rest_framework.routers import DefaultRouter
from apps.account.views import (
    RoleViewSet,
    UserViewSet,
    # CompanyProfileViewSet,
    PasswordChangeViewSet
)

router = DefaultRouter()

router.register('roles', RoleViewSet, basename='roles')
router.register('users', UserViewSet, 'users')
# router.register('company-profile', CompanyProfileViewSet, 'company-profile')
router.register('change-password', PasswordChangeViewSet, 'change-password')

urlpatterns = router.urls
