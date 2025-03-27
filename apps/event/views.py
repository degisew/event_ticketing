from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from apps.event.permissions import (
    EventAccessPolicy,
    PaymentAccessPolicy,
    ReservationAccessPolicy,
    TicketAccessPolicy,

)
from apps.event.filters import EventFilter, TicketFilter, ReservationFilter
from apps.event.models import Event, Payment, Reservation, Ticket
from apps.core.views import AbstractModelViewSet
from apps.event.serializers import (
    EventSerializer,
    PaymentSerializer,
    ReservationSerializer,
    TicketResponseSerializer
)


class EventViewSet(AbstractModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_classes = [EventFilter]


# TODO: Tickets should not be created directly.
# TODO: They should be created when a reservation is made.
class TickerViewSet(AbstractModelViewSet):
    permission_classes = [TicketAccessPolicy]
    http_method_names = ['get']
    serializer_class = TicketResponseSerializer
    queryset = Ticket.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_classes = [TicketFilter]


class ReservationViewSet(AbstractModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_classes = [ReservationFilter]


class PaymentViewSet(AbstractModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post']
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
