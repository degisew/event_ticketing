from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filters
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet
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
    ReservationSerializer,
    TicketResponseSerializer,
    TransactionResponseSerializer,
)
from apps.event.services import ReservationService


@method_decorator(cache_page(60 * 15), name="list")
@method_decorator(cache_page(60 * 15), name="retrieve")
class EventViewSet(AbstractModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_classes = [EventFilter]


class TicketViewSet(AbstractModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ["get"]
    serializer_class = TicketResponseSerializer
    queryset = Ticket.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_classes = [TicketFilter]


@method_decorator(cache_page(60 * 15), name="list")
@method_decorator(cache_page(60 * 15), name="retrieve")
class TicketTypeViewSet(AbstractModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = TicketTypeSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_classes = [TicketTypeFilter]

    def get_queryset(self):
        event_pk = self.kwargs.get("event_pk")
        return TicketType.objects.select_related("category").filter(event=event_pk)

    def perform_create(self, serializer):
        event_pk = self.kwargs.get("event_pk")
        event = get_object_or_404(Event, id=event_pk)
        serializer.save(event=event)


class ReservationViewSet(AbstractModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ReservationSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_classes = [ReservationFilter]

    def get_queryset(self):
        event_pk = self.kwargs.get("event_pk")
        return Reservation.objects.select_related(
            "user", "ticket_type__category", "payment_status", "status"
        ).filter(event=event_pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        event_pk = self.kwargs.get("event_pk")
        event = get_object_or_404(Event, id=event_pk)
        context["event"] = event

        return context

    @action(methods=["POST"], detail=True)
    def pay(self, request, event_pk=None, pk=None):
        try:
            reservation = self.get_object()
            response = ReservationService.process_payment(reservation)
            return Response(
                {
                    "message": "Payment processed successfully.",
                    "transaction": TransactionResponseSerializer(response).data,
                    "status": status.HTTP_200_OK,
                }
            )
        # TODO: Proper handling here
        except Exception as e:
            raise e


class TransactionViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = TransactionResponseSerializer
    queryset = Transaction.objects.select_related("reservation__event").all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["reservation__event__id"]
