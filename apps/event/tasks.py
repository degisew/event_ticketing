import logging
from django.conf import settings
from django.db import transaction
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from celery import shared_task
from apps.core.services import DataLookupService
from apps.event.models import Reservation
from apps.event.utils import generate_qr_code
from apps.event.enums import (
    ReservationStatuses,
    TicketTypeUpdateFlags,
    RESERVATION_STATUS_TYPE,
)


logger = logging.getLogger(__name__)


@shared_task
def send_ticket_email(tickets_data, recipient_email, event):
    subject = f"Your Tickets for {event}"
    message = (
        f"Dear {recipient_email[0]},\n\n"
        f"Thank you for your reservation for the {event} event.\n"
        f"We've attached your tickets below as a QR code.\n\n"
        "We look forward to seeing you at the event!\n\n"
        "Best regards,\n"
        "The Team"
    )

    email = EmailMessage(
        subject, message, settings.DEFAULT_FROM_EMAIL, to=recipient_email
    )

    # Loop through the tickets and generate a QR code for each
    for ticket_number in tickets_data:
        ticket_info = f"Ticket ID: {ticket_number}"

        # Generate the QR code for each ticket
        qr_image = generate_qr_code(ticket_info)

        # Attach QR Code to Email
        email.attach(f"ticket_qr_{ticket_number}.png", qr_image.getvalue(), "image/png")

    # Send the email
    email.send()


@shared_task
def expire_reservation_task(reservation_id):
    try:
        with transaction.atomic():
            reservation = Reservation.objects.select_for_update().get(id=reservation_id)

            reservation_pending_status = DataLookupService.get_cached_lookup(
                type=RESERVATION_STATUS_TYPE, value=ReservationStatuses.PENDING.value
            )

            if reservation.status != reservation_pending_status:
                logger.info(
                    f"Reservation {reservation_id} is not pending; skipping expiry."
                )
                return

            reservation_expired_status = DataLookupService.get_cached_lookup(
                type=RESERVATION_STATUS_TYPE, value=ReservationStatuses.EXPIRED.value
            )

            reservation.status = reservation_expired_status
            reservation.save(update_fields=["status"])

            reservation.ticket_type.update_available_tickets(
                reservation.ticket_quantity, flag=TicketTypeUpdateFlags.INCREMENT.value
            )

            logger.info(
                f"Expired reservation {reservation_id} and updated ticket availability."
            )

    except ObjectDoesNotExist:
        logger.warning(f"Reservation {reservation_id} not found during expiry task.")
    except Exception as e:
        logger.error(f"Error expiring reservation {reservation_id}. {e}", exc_info=True)
        raise
