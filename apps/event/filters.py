from django_filters import rest_framework as filters
from apps.event.models import Event, Reservation, Ticket, TicketType, Transaction


class EventFilter(filters.FilterSet):
    class Meta:
        model = Event
        fields = ["start_date", "is_active"]


class TicketFilter(filters.FilterSet):
    class Meta:
        model = Ticket
        fields = ["ticket_number", "reservation"]


class TicketTypeFilter(filters.FilterSet):
    category_name = filters.CharFilter(field_name="category__name")

    class Meta:
        model = TicketType
        fields = ["category_name", "event"]


class ReservationFilter(filters.FilterSet):
    class Meta:
        model = Reservation
        fields = ["reserved_date", "payment_status", "status"]


class TransactionFilter(filters.FilterSet):
    event_id = filters.CharFilter(field_name="reservation__event__id")

    class Meta:
        model = Transaction
        fields = ["event_id"]
