from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from apps.core.views import AbstractModelViewSet
from apps.event.filters import (
    EventFilter,
    TicketFilter,
    TicketTypeFilter,
    ReservationFilter,
)
from apps.event.models import Event, TicketType, Transaction, Reservation, Ticket
from apps.event.serializers import (
    EventSerializer,
    TicketTypeSerializer,
    TransactionSerializer,
    ReservationSerializer,
    TicketResponseSerializer,
)


@method_decorator(cache_page(60 * 15), name="list")
@method_decorator(cache_page(60 * 15), name="retrieve")
class EventViewSet(AbstractModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_classes = [EventFilter]


class TicketViewSet(AbstractModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ["get"]
    serializer_class = TicketResponseSerializer
    queryset = Ticket.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_classes = [TicketFilter]


@method_decorator(cache_page(60 * 15), name="list")
@method_decorator(cache_page(60 * 15), name="retrieve")
class TicketTypeViewSet(AbstractModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = TicketTypeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_classes = [TicketTypeFilter]
    queryset = TicketType.objects.select_related("category", "event").all()


class ReservationViewSet(AbstractModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_classes = [ReservationFilter]
    queryset = Reservation.objects.select_related(
        "user", "ticket_type__category", "payment_status", "status"
    ).all()


class TransactionViewSet(AbstractModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ["get", "post"]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.select_related("reservation__event").all()
