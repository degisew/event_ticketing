from rest_framework_nested import routers
from apps.event.views import (
    EventViewSet,
    ReservationViewSet,
    TicketTypeViewSet,
    TransactionViewSet,
)


router = routers.SimpleRouter()  # type: ignore

router.register(r"events", EventViewSet, basename="events")

events_router = routers.NestedSimpleRouter(router, "events", lookup="event")

events_router.register(r"ticket_types", TicketTypeViewSet, basename="ticket_types")

events_router.register(r"reservations", ReservationViewSet, basename="reservations")

router.register(r"transactions", TransactionViewSet, basename="transactions")


urlpatterns = router.urls + events_router.urls
