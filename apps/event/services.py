import logging
from django.utils import timezone
from django.db import transaction, IntegrityError, DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from apps.core.models import DataLookup
from apps.event.enums import (
    ReservationPaymentStatuses,
    RESERVATION_PAYMENT_STATUS_TYPE,
    ReservationStatuses,
    RESERVATION_STATUS_TYPE,
    TicketStatuses,
    TICKET_STATUS_TYPE,
)
from apps.event.exceptions import (
    DataIntegrityError,
    EventNotAvailableError,
    NotEnoughSeatsAvailableError,
)
from apps.event.models import TicketType, Transaction, Reservation, Ticket
from apps.core.utils import generate_unique_code
from apps.event.tasks import send_ticket_email

logger = logging.getLogger(__name__)


class ReservationService:
    @staticmethod
    @transaction.atomic
    def create_reservation(validated_data) -> Reservation:
        """
        Create a reservation with comprehensive error handling

        Args:
            validated_data: Validated reservation data

        Returns:
            Reservation: Created reservation instance

        Raises:
            NotEnoughSeatsAvailableError: When insufficient seats available
            EventNotAvailableError: When event is not available
            DataIntegrityError: When data consistency issues occur
        """
        ticket_type = validated_data["ticket_type"]
        ticket_quantity = validated_data["ticket_quantity"]
        user = validated_data["user"]
        event = validated_data["event"]

        logger.info(
            f"Starting reservation creation for user {user.id}, event {event.id}"
        )

        ReservationService._validate_reservation_business_rules(
            event, ticket_type, ticket_quantity
        )

        # Get or create lookup data
        payment_status, status = ReservationService._get_reservation_statuses()

        if ticket_type.available_tickets < ticket_quantity:
            raise NotEnoughSeatsAvailableError("Not enough seats available.")

        code = generate_unique_code("RSVP", "")

        reservation = Reservation.objects.create(
            payment_status=payment_status, status=status, code=code, **validated_data
        )

        # update available seats
        ReservationService._update_ticket_availability(ticket_type, ticket_quantity)

        logger.info(
            f"{user.email} successfully reserved {ticket_quantity} tickets for event {event.id}"
        )

        return reservation

    @staticmethod
    def _validate_reservation_business_rules(event, ticket_type, ticket_quantity):
        # Check if event is available for reservation
        if not event.is_active or event.start_date < timezone.now():
            raise EventNotAvailableError("Event is no longer available for reservation")

        # Check seat availability
        if ticket_type.available_tickets < ticket_quantity:
            raise NotEnoughSeatsAvailableError(
                detail={
                    "message": f"Only {ticket_type.available_tickets} seats available.",
                    "available": ticket_type.available_tickets,
                    "requested": ticket_quantity,
                }
            )

    @staticmethod
    def _get_reservation_statuses():
        """Get or create reservation status lookup data"""
        try:
            payment_status = DataLookup.objects.get(
                type=RESERVATION_PAYMENT_STATUS_TYPE,
                value=ReservationPaymentStatuses.PENDING.value,
            )

            status = DataLookup.objects.get(
                type=RESERVATION_STATUS_TYPE, value=ReservationStatuses.PENDING.value
            )

            return payment_status, status

        except DataLookup.DoesNotExist as e:
            logger.error(f"Required lookup data not found: {str(e)}")
            raise DataIntegrityError(
                detail={"System configuration error: Required status data not found"}
            )

    # TODO: Use this method for both updations using a flag (
    # TODO: decrementing for paid and increment for revocked reservations)
    @staticmethod
    def _update_ticket_availability(ticket_type, quantity):
        try:
            # Use select_for_update to prevent race conditions
            updated_ticket_type = TicketType.objects.select_for_update().get(
                id=ticket_type.id
            )

            if updated_ticket_type.available_tickets < quantity:
                raise NotEnoughSeatsAvailableError(
                    detail={
                        "available": updated_ticket_type.available_tickets,
                        "requested": quantity,
                    }
                )

            updated_ticket_type.update_available_tickets(quantity)

        except ObjectDoesNotExist:
            logger.error(f"Ticket type {ticket_type.id} not found during update")
            raise DataIntegrityError("Ticket type no longer exists")


class TransactionService:
    @staticmethod
    def _calculate_total_amount(reservation):
        if reservation.ticket_type:
            price = reservation.ticket_type.price
            return price * reservation.ticket_quantity
        raise AttributeError

    @staticmethod
    def _create_transaction_record(reservation, amount):
        try:
            return Transaction.objects.create(reservation=reservation, amount=amount)
        except IntegrityError as e:
            raise e
        except DatabaseError as e:
            raise e

    @staticmethod
    def _create_single_ticket(ticket_type, reservation) -> Ticket:
        return Ticket.objects.create(
            reservation=reservation,
            ticket_number=generate_unique_code("TKT", reservation.id),
            status=DataLookup.objects.get(
                type=TICKET_STATUS_TYPE, value=TicketStatuses.SOLD.value
            ),
            unit_price=ticket_type.price,
        )

    @staticmethod
    def _create_tickets(reservation):
        if not reservation.user:
            raise KeyError("Reservation has no associated user.")

        if not reservation.ticket_quantity:
            raise KeyError("Reservation has no key ticket_quantity.")

        ticket_type = reservation.ticket_type
        quantity = reservation.ticket_quantity

        tickets = []
        for _ in range(quantity):
            ticket = TransactionService._create_single_ticket(ticket_type, reservation)
            tickets.append(ticket.ticket_number)
        return tickets

    @staticmethod
    def _get_reservation_statuses():
        """Get or create reservation status lookup data"""
        try:
            payment_status = DataLookup.objects.get(
                type=RESERVATION_PAYMENT_STATUS_TYPE,
                value=ReservationPaymentStatuses.PAID.value,
            )

            status = DataLookup.objects.get(
                type=RESERVATION_STATUS_TYPE, value=ReservationStatuses.COMPLETED.value
            )

            return payment_status, status

        except DataLookup.DoesNotExist as e:
            logger.error(f"Required lookup data not found: {str(e)}")
            raise DataIntegrityError(
                detail={"System configuration error: Required status data not found"}
            )

    @staticmethod
    def _update_reservation_status(reservation):
        payment_status, status = TransactionService._get_reservation_statuses()

        reservation.payment_status = payment_status
        reservation.status = status

        reservation.save()

    @staticmethod
    @transaction.atomic
    def transaction_handler(validated_data):
        reservation = validated_data["reservation"]

        tickets = TransactionService._create_tickets(reservation)

        TransactionService._update_reservation_status(reservation)

        total_amount = TransactionService._calculate_total_amount(reservation)

        payment = TransactionService._create_transaction_record(
            reservation, total_amount
        )

        if tickets:
            recipient_email = [reservation.user.email]

            # Trigger the Celery task in the background
            send_ticket_email.delay(tickets, recipient_email, reservation.event.name)

        return payment
