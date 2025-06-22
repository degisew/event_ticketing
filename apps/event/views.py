from django_filters.rest_framework import DjangoFilterBackend
from apps.event.permissions import (
    EventAccessPolicy,
    TransactionAccessPolicy,
    ReservationAccessPolicy,
    TicketAccessPolicy,
    TicketTypeAccessPolicy,
)
from apps.event.filters import (
    EventFilter,
    TicketFilter,
    TicketTypeFilter,
    ReservationFilter,
)
from apps.event.models import Event, TicketType, Transaction, Reservation, Ticket
from apps.core.views import AbstractModelViewSet
from apps.event.serializers import (
    EventSerializer,
    TicketTypeSerializer,
    TransactionSerializer,
    ReservationSerializer,
    TicketResponseSerializer,
)


class EventViewSet(AbstractModelViewSet):
    permission_classes = [EventAccessPolicy]
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_classes = [EventFilter]


class TicketViewSet(AbstractModelViewSet):
    permission_classes = [TicketAccessPolicy]
    http_method_names = ["get"]
    serializer_class = TicketResponseSerializer
    queryset = Ticket.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_classes = [TicketFilter]


class TicketTypeViewSet(AbstractModelViewSet):
    permission_classes = [TicketTypeAccessPolicy]
    serializer_class = TicketTypeSerializer
    queryset = TicketType.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_classes = [TicketTypeFilter]


class ReservationViewSet(AbstractModelViewSet):
    permission_classes = [ReservationAccessPolicy]
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_classes = [ReservationFilter]


class TransactionViewSet(AbstractModelViewSet):
    permission_classes = [TransactionAccessPolicy]
    http_method_names = ["get", "post"]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
