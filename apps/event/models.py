from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import AbstractBaseModel, DataLookup


class Event(AbstractBaseModel):
    name = models.CharField(verbose_name=_("Event Name"), max_length=255)

    code = models.CharField(verbose_name=_("Event Code"), max_length=50, unique=True)

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name="events",
        verbose_name=_("Event Organizer")
    )

    description = models.TextField(verbose_name=_("Event Description"))

    start_date = models.DateTimeField(
        verbose_name=_("Start Date"), help_text=_("Format: YYYY-MM-DD HH:MM:SS")
    )

    end_date = models.DateTimeField(
        verbose_name=_("End Date"), help_text=_("Format: YYYY-MM-DD HH:MM:SS")
    )

    location = models.CharField(verbose_name=_("Location"), max_length=255)

    is_active = models.BooleanField(verbose_name=_("Is Active"), default=True)

    capacity = models.PositiveIntegerField(verbose_name=_("Capacity"), default=0)

    available_seats = models.PositiveIntegerField(
        verbose_name=_("Available Seats"), default=0
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        db_table = "events"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "start_date"], name="unique_event_start"
            )
        ]

    def save(self, *args, **kwargs):
        """Set available seats to capacity when creating an event for the first time."""
        # Only set if event is being created (not updated)
        if self._state.adding:
            self.available_seats = self.capacity
        super().save(*args, **kwargs)

    def update_available_seats(self, seats: int):
        """Update the available seats for the event."""
        self.available_seats -= seats
        self.save()

    def __str__(self) -> str:
        return self.name


class Reservation(AbstractBaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="reservations",
        on_delete=models.CASCADE
    )

    event = models.ForeignKey(
        Event, related_name="reservations", on_delete=models.CASCADE
    )

    code = models.CharField(
        verbose_name=_("Code"),
        max_length=100,
        unique=True
    )

    reserved_date = models.DateTimeField(
        verbose_name=_("Reserved Date"), auto_now_add=True
    )

    status = models.ForeignKey(
        DataLookup,
        on_delete=models.RESTRICT,
        limit_choices_to={"type": "reservation_status"},
        related_name="+",
        verbose_name=_("Status")     
    )

    payment_status = models.ForeignKey(
        DataLookup,
        on_delete=models.RESTRICT,
        limit_choices_to={"type": "reservation_payment_status"},
        related_name="+",
        verbose_name=_("Payment Status"),
        max_length=10,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")
        db_table = "reservations"

    def __str__(self) -> str:
        return f"Reservation for {self.user} at {self.event.name}"


class Ticket(AbstractBaseModel):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name=_("Event"),
    )

    ticket_number = models.CharField(
        verbose_name=_("Ticket Number"), max_length=255, unique=True
    )

    seat_number = models.CharField(
        verbose_name=_("Seat Number"), max_length=50, blank=True, null=True
    )

    status = models.ForeignKey(
        DataLookup,
        on_delete=models.RESTRICT,
        limit_choices_to={"type": "ticket_status"},
        related_name="+",
        verbose_name=_("Status")
    )

    unit_price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")
        db_table = "tickets"

    def __str__(self) -> str:
        return f"{self.event.name} - {self.ticket_number}"


class ReservationItem(AbstractBaseModel):
    reservation = models.ForeignKey(
        Reservation, related_name="reservation_items", on_delete=models.CASCADE, verbose_name=_("Reservation")
    )

    ticket = models.ForeignKey(
        Ticket, related_name="reservation_items", on_delete=models.CASCADE, verbose_name=_("Ticket")
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Reservation Item")
        verbose_name_plural = _("Reservation Items")
        db_table = "reservation_items"
        constraints = [
            models.UniqueConstraint(
                fields=["reservation", "ticket"], name="unique_ticket_per_reservation"
            )
        ]

    def __str__(self) -> str:
        return f"Ticket {self.ticket.ticket_number} for {self.reservation.event.name}"


# ? Can we change this name to PaymentTransaction?
class Payment(AbstractBaseModel):
    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name="payment",
        verbose_name=_("Reservation")
    )

    amount = models.DecimalField(
        verbose_name=_("Amount"),
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateTimeField(
        verbose_name=_("Payment Date"),
        help_text=_("Format: YYYY-MM-DD HH:MM:SS"),
        auto_now_add=True,
    )

    # ? How will it be? Will it be a dropdown or a text field
    payment_method = models.CharField(
        verbose_name=_("Payment Method"),
        max_length=50
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        db_table = "payments"

    def __str__(self) -> str:
        return f"Payment for {self.reservation} - {self.amount}"
