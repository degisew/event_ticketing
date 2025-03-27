from decimal import Decimal
from django.db import transaction
from django.db import transaction, IntegrityError, DatabaseError
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from apps.core.models import DataLookup
from apps.event.enums import (
    ReservationPaymentStatuses,
    ReservationStatuses,
    TicketStatuses,
)
from apps.event.exceptions import NotEnoughSeatsAvailableError
from apps.event.models import Payment, Reservation, ReservationItem, Ticket
from apps.core.utils import generate_unique_code


class ReservationService:
    @staticmethod
    @transaction.atomic
    def create_reservation(validated_data) -> Reservation:
        print("#####", validated_data)
        event = validated_data["event"]
        seats = validated_data.pop("quantity")

        print("#####", validated_data)

        if event.available_seats < seats:
            raise NotEnoughSeatsAvailableError("Not enough seats available.")

        try:
            payment_status = DataLookup.objects.get(
                type="reservation_payment_status",
                value=ReservationPaymentStatuses.PENDING.value,
            )

            status = DataLookup.objects.get(
                type="reservation_status", value=ReservationStatuses.PENDING.value
            )
        except DataLookup.DoesNotExist:
            # TODO: Ensure this is needed like this or raise error instead.
            payment_status = DataLookup.objects.create(
                type="reservation_payment_status",
                value=ReservationPaymentStatuses.PENDING.value,
            )

            status = DataLookup.objects.create(
                type="reservation_status", value=ReservationStatuses.PENDING.value
            )
        try:
            code = generate_unique_code("RSVP", "")
            reservation = Reservation.objects.create(
                payment_status=payment_status,
                status=status,
                code=code,
                **validated_data
            )

            # update available seats
            event.update_available_seats(seats)

            tickets = ReservationService.create_tickets(event, reservation, seats)
            reservation_items = ReservationService.create_reservation_items(
                reservation, tickets
            )

            print(
                {
                    "reservation": reservation,
                    "tickets": tickets,
                    "reservation_items": reservation_items,
                }
            )
            return reservation
        except Exception as e:
            raise e

    # def cancel_reservation(self, reservation):
    #     reservation.event.available_seats += reservation.seats
    #     reservation.event.save()
    #     reservation.delete()

    # TODO: Fix seat number generation issue
    @staticmethod
    def create_single_ticket(i, event, reservation) -> Ticket:
        print("111", event.capacity - event.available_seats)
        seat_number = event.capacity - event.available_seats + i
        return Ticket.objects.create(
            event=event,
            ticket_number=generate_unique_code("TKT", reservation.id),
            seat_number=f"SEAT {seat_number}",
            status=DataLookup.objects.get(
                type=TicketStatuses.TYPE.value, value=TicketStatuses.ACTIVE.value
            ),
            # TODO: Update this to be dynamic
            unit_price=Decimal("200.00"),
        )

    @staticmethod
    def create_tickets(event, reservation, quantity):
        tickets = []
        for i in range(1, quantity + 1):
            ticket = ReservationService.create_single_ticket(i, event, reservation)
            tickets.append(ticket)
        return tickets

    @staticmethod
    def create_reservation_items(reservation, tickets):
        items = []
        for ticket in tickets:
            item = ReservationItem.objects.create(
                reservation=reservation, ticket=ticket
            )
            items.append(item)

        return items


class PaymentService:
    @staticmethod
    def calculate_total_amount(reservation):
        try:
            total_amount = ReservationItem.objects.filter(
                reservation=reservation
            ).aggregate(total_amount=Sum('ticket__unit_price'))["total_amount"]
            return total_amount or 0
        except DatabaseError as e:
            raise e

    @staticmethod
    def create_payment_record(reservation, amount):
        try:
            return Payment.objects.create(reservation=reservation, amount=amount)
        except IntegrityError as e:
            raise e
        except DatabaseError as e:
            raise e

    @staticmethod
    def update_reservation_status(reservation):
        try:
            reservation.payment_status = DataLookup.objects.get(
                type="reservation_payment_status",
                value=ReservationPaymentStatuses.PAID.value,
            )
            reservation.status = DataLookup.objects.get(
                type="reservation_status",
                value=ReservationStatuses.COMPLETED.value,
            )
            reservation.save()
        except ObjectDoesNotExist:
            raise ValueError("Invalid payment status lookup.")
        except DatabaseError as e:
            raise e

    @staticmethod
    def update_ticket_statuses(reservation):
        try:
            tickets = list(Ticket.objects.filter(
                id__in=reservation.reservation_items.values_list('ticket_id', flat=True)
            ))

            if not tickets:
                return

            sold_status = DataLookup.objects.get(
                type=TicketStatuses.TYPE.value, value=TicketStatuses.SOLD.value
            )

            for ticket in tickets:
                ticket.status = sold_status

            Ticket.objects.bulk_update(tickets, ["status"])
        except ObjectDoesNotExist:
            raise ValueError("Invalid ticket status lookup.")
        except DatabaseError as e:
            raise e

    @staticmethod
    @transaction.atomic
    def process_payment(validated_data):
        try:
            reservation = validated_data["reservation"]

            total_amount = PaymentService.calculate_total_amount(reservation)
            payment = PaymentService.create_payment_record(reservation, total_amount)
            PaymentService.update_reservation_status(reservation)
            PaymentService.update_ticket_statuses(reservation)

            return payment

        except Exception as e:
            raise e
