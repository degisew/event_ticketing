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
        verbose_name=_("Event Organizer"),
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

    class Meta:
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


class TicketType(AbstractBaseModel):
    """
    Represents a reusable ticket type(e.g., VIP, Early Bird, General Admission)
    tailored to organizer needs.

    Instead of storing ticket type names and descriptions repeatedly
    across events, the fields 'category' references a centralized
    lookup (via `DataLookup`) that holds common ticket type definitions.
    This promotes consistency, reduces redundancy, and helps prevent
    human errors (e.g., typos or naming variations like 'VIP' vs 'V.I.P').

    Attributes:
        category (ForeignKey): A reference to a predefined
        ticket type entry in the DataLookup table.

    Inherits From:
        AbstractBaseModel: A base model providing common
        fields like 'id', 'created_at', 'updated_at', etc.
    """

    category = models.ForeignKey(
        DataLookup,
        on_delete=models.CASCADE,
        limit_choices_to={"type": "ticket_type"},
        related_name="+",
        verbose_name=_("Ticket Category"),
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name=_("Event"),
        related_name="ticket_types",
    )

    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Price")
    )

    total_tickets = models.PositiveIntegerField(verbose_name=_("Total Tickets"))

    available_tickets = models.PositiveIntegerField(verbose_name=_("Available Tickets"))

    class Meta:
        verbose_name = _("Ticket Type")
        verbose_name_plural = _("Ticket Types")
        db_table = "ticket_types"

    def save(self, *args, **kwargs):
        """Set available tickets to total tickets when
        creating an event for the first time only."""
        # Only set if event is being created (not updated)
        if self._state.adding:
            self.available_tickets = self.total_tickets
        super().save(*args, **kwargs)

    def update_available_tickets(self, quantity: int):
        self.available_tickets -= quantity
        self.save()

    def __str__(self) -> str:
        return f"{self.price} for {self.category.name} ticket"


class Reservation(AbstractBaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="reservations", on_delete=models.CASCADE
    )

    event = models.ForeignKey(
        Event, related_name="reservations", on_delete=models.CASCADE
    )

    ticket_type = models.ForeignKey(
        TicketType,
        on_delete=models.CASCADE,
        related_name="reservation",
        verbose_name=_("Ticket Type"),
    )

    ticket_quantity = models.PositiveIntegerField(verbose_name=_("Ticket Quantity"))

    code = models.CharField(unique=True, max_length=100, verbose_name=_("Code"))

    reserved_date = models.DateTimeField(
        verbose_name=_("Reserved Date"), auto_now_add=True
    )

    status = models.ForeignKey(
        DataLookup,
        on_delete=models.RESTRICT,
        limit_choices_to={"type": "reservation_status"},
        related_name="+",
        verbose_name=_("Status"),
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
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")
        db_table = "reservations"

    def __str__(self) -> str:
        return f"Reservation for {self.user.email} at {self.event.name}"


class Ticket(AbstractBaseModel):
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.PROTECT,
        related_name="tickets",
        verbose_name=_("Reservation"),
    )

    ticket_number = models.CharField(
        verbose_name=_("Ticket Number"), max_length=255, unique=True
    )

    status = models.ForeignKey(
        DataLookup,
        on_delete=models.RESTRICT,
        limit_choices_to={"type": "ticket_status"},
        related_name="+",
        verbose_name=_("Status"),
    )

    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Unit Price")
    )

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")
        db_table = "tickets"

    def __str__(self) -> str:
        return f"{self.ticket_number}"


class Transaction(AbstractBaseModel):
    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name="transaction",
        verbose_name=_("Reservation"),
    )

    amount = models.DecimalField(
        verbose_name=_("Amount"), max_digits=10, decimal_places=2
    )

    transaction_date = models.DateTimeField(
        verbose_name=_("Transaction Date"),
        help_text=_("Format: YYYY-MM-DD HH:MM:SS"),
        auto_now_add=True,
    )

    # * Will be auto tracked from user activity
    payment_method = models.CharField(verbose_name=_("Payment Method"), max_length=50)

    class Meta:
        verbose_name = _("transaction")
        verbose_name_plural = _("transactions")
        db_table = "transactions"

    def __str__(self) -> str:
        return f"Payment transaction for {self.reservation} - {self.amount}"
