from django_filters import FilterSet
# from django_filters import rest_framework as filters
from apps.event.models import Event, Reservation, Ticket


class EventFilter(FilterSet):
    class Meta:
        model = Event
        fields = ['start_date', 'is_active']


class TicketFilter(FilterSet):
    class Meta:
        model = Ticket
        fields = ['seat_number', 'event']


class ReservationFilter(FilterSet):
    class Meta:
        model = Reservation
        fields = ['reserved_date', 'payment_status', 'status']
