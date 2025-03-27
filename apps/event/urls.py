from rest_framework.routers import DefaultRouter

from apps.event.views import (
    EventViewSet,
    ReservationViewSet,
    PaymentViewSet
)
router = DefaultRouter()

router.register(r'events', EventViewSet, basename='events')
# router.register(r'tickets', TickerViewSet, basename='tickets')
router.register(r'reservations', ReservationViewSet, basename='reservations')
router.register(r'payments', PaymentViewSet, basename='payments')

urlpatterns = router.urls
