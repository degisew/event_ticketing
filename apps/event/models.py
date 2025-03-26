from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import AbstractBaseModel


class Event(AbstractBaseModel):
    name = models.CharField(verbose_name=_("Event Name"), max_length=255)
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
    price = models.DecimalField(
        verbose_name=_("Price"), max_digits=10, decimal_places=2
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

    def __str__(self) -> str:
        return self.name


class Reservation(AbstractBaseModel):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="reservations", on_delete=models.CASCADE
    )

    event = models.ForeignKey(
        Event, related_name="reservations", on_delete=models.CASCADE
    )

    reserved_date = models.DateTimeField(
        verbose_name=_("Reserved Date"), auto_now_add=True
    )

    status = models.CharField(
        verbose_name=_("Status"),
        max_length=10,
        choices=[
            ("active", _("Active")),
            ("expired", _("Expired")),
            ("canceled", _("Canceled")),
        ],
        default="active",
    )

    total_price = models.DecimalField(
        verbose_name=_("Total Price"), max_digits=10, decimal_places=2
    )

    payment_status = models.CharField(
        verbose_name=_("Payment Status"),
        max_length=10,
        choices=[("pending", _("Pending")), ("completed", _("Completed"))],
        default="pending",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")
        db_table = "reservations"

    def __str__(self) -> str:
        return f"Reservation for {self.customer} at {self.event.name}"


class Ticket(AbstractBaseModel):
    event = models.ForeignKey(Event, related_name="tickets", on_delete=models.CASCADE)

    ticket_number = models.CharField(
        verbose_name=_("Ticket Number"), max_length=255, unique=True
    )

    seat_number = models.CharField(
        verbose_name=_("Seat Number"), max_length=50, blank=True, null=True
    )

    status = models.CharField(
        verbose_name=_("Status"),
        max_length=10,
    )

    reservation = models.ForeignKey(
        Reservation,
        related_name="tickets",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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
        Reservation, related_name="reservation_items", on_delete=models.CASCADE
    )

    ticket = models.ForeignKey(
        Ticket, related_name="reservation_items", on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"), default=0)

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
        return f"{self.quantity} tickets for {self.reservation}"


class Payment(AbstractBaseModel):
    reservation = models.OneToOneField(
        Reservation, related_name="payment", on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        verbose_name=_("Amount"), max_digits=10, decimal_places=2
    )

    payment_date = models.DateTimeField(
        verbose_name=_("Payment Date"),
        help_text=_("Format: YYYY-MM-DD HH:MM:SS"),
        auto_now_add=True,
    )

    payment_method = models.CharField(verbose_name=_("Payment Method"), max_length=50)

    payment_status = models.CharField(
        verbose_name=_("Payment Status"),
        max_length=10,
        choices=[("pending", _("Pending")), ("completed", _("Completed"))],
        default="pending",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        db_table = "payments"

    def __str__(self) -> str:
        return f"Payment for {self.reservation} - {self.amount}"
