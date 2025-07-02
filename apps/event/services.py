import logging
from uuid import UUID
from django.core.cache import cache
from django.utils import timezone
from django.db import transaction, IntegrityError, DatabaseError
from apps.event.enums import (
    ReservationPaymentStatuses,
    RESERVATION_PAYMENT_STATUS_TYPE,
    ReservationStatuses,
    RESERVATION_STATUS_TYPE,
    TicketStatuses,
    TICKET_STATUS_TYPE,
    TicketTypeUpdateFlags,
)
from apps.core.exceptions import DataIntegrityError
from apps.event.exceptions import (
    EventNotAvailableError,
    NotEnoughSeatsAvailableError,
)
from apps.event.models import TicketType, Transaction, Reservation, Ticket
from apps.core.utils import generate_unique_code
from apps.core.services import DataLookupService
from apps.event.tasks import send_ticket_email, expire_reservation_task

logger = logging.getLogger(__name__)


class TicketTypeService:
    @staticmethod
    def get_cached_ticket_type(id: UUID):
        key = f"ticket_type_{id}"

        result = cache.get(key)

        if not result:
            try:
                result = TicketType.objects.select_for_update().get(id=id)
                cache.set(key, result, timeout=3600)
            except TicketType.DoesNotExist as e:
                logger.error(str(e))
                raise DataIntegrityError("Ticket Type not found")
        return result


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

        payment_status = DataLookupService.get_cached_lookup(
            RESERVATION_PAYMENT_STATUS_TYPE, ReservationPaymentStatuses.PENDING.value
        )

        status = DataLookupService.get_cached_lookup(
            RESERVATION_STATUS_TYPE, ReservationStatuses.PENDING.value
        )

        code = generate_unique_code("RSVP", "")

        reservation = Reservation.objects.create(
            payment_status=payment_status, status=status, code=code, **validated_data
        )

        # update available seats
        ReservationService._update_ticket_availability(
            ticket_type, ticket_quantity, flag=TicketTypeUpdateFlags.DECREMENT.value
        )

        # scheduling expiration
        expire_reservation_task.apply_async(args=[reservation.id], countdown=1 * 60)

        logger.info(
            f"{user.email} successfully reserved {ticket_quantity} tickets for event {event.id}"
        )

        return reservation

    @staticmethod
    def _validate_reservation_business_rules(event, ticket_type, ticket_quantity):
        # Check if event is available for reservation
        if not event.is_active or event.start_date < timezone.now():
            raise EventNotAvailableError("Event is no longer available for reservation")

        tickets_available: int = ticket_type.available_tickets

        # Check seat availability
        if tickets_available < ticket_quantity:
            raise NotEnoughSeatsAvailableError(
                detail={
                    "message": f"Only {tickets_available} seats available.",
                    "available": tickets_available,
                    "requested": ticket_quantity,
                }
            )

    @staticmethod
    def _update_ticket_availability(ticket_type, quantity, flag):
        updated_ticket_type = TicketTypeService.get_cached_ticket_type(ticket_type.id)

        updated_ticket_type.update_available_tickets(
            quantity, flag=TicketTypeUpdateFlags.DECREMENT.value
        )

    @staticmethod
    def _calculate_total_amount(reservation):
        ticket_type = reservation.ticket_type
        if ticket_type:
            return ticket_type.price * reservation.ticket_quantity
        raise AttributeError

    @staticmethod
    # TODO: Proper Eror handling
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
            status=DataLookupService.get_cached_lookup(
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
            ticket = ReservationService._create_single_ticket(ticket_type, reservation)
            tickets.append(ticket.ticket_number)
        return tickets

    @staticmethod
    def _update_reservation_status(reservation, payment_status, status):
        reservation.payment_status = payment_status
        reservation.status = status

        reservation.save()

    @staticmethod
    @transaction.atomic
    def process_payment(reservation):
        tickets = ReservationService._create_tickets(reservation)

        payment_status = DataLookupService.get_cached_lookup(
            RESERVATION_PAYMENT_STATUS_TYPE, ReservationPaymentStatuses.PAID.value
        )

        status = DataLookupService.get_cached_lookup(
            RESERVATION_STATUS_TYPE, ReservationStatuses.COMPLETED.value
        )

        total_amount = ReservationService._calculate_total_amount(reservation)

        ReservationService._update_reservation_status(
            reservation, payment_status, status
        )

        transaction = ReservationService._create_transaction_record(
            reservation, total_amount
        )

        if tickets:
            recipient_email = [reservation.user.email]

            # Trigger the Celery task in the background
            send_ticket_email.delay(tickets, recipient_email, reservation.event.name)

        return transaction
