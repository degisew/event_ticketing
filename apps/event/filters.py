from django_filters import FilterSet
from apps.event.models import Event, Reservation, Ticket, TicketType


class EventFilter(FilterSet):
    class Meta:
        model = Event
        fields = ["start_date", "is_active"]


class TicketFilter(FilterSet):
    class Meta:
        model = Ticket
        fields = ["ticket_number", "reservation"]


class TicketTypeFilter(FilterSet):
    class Meta:
        model = TicketType
        fields = ["category__name", "event"]


class ReservationFilter(FilterSet):
    class Meta:
        model = Reservation
        fields = ["reserved_date", "payment_status", "status"]
