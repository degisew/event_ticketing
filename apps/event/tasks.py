# from django.core.mail import send_mail
# from io import BytesIO
from django.conf import settings
from django.core.mail import EmailMessage
from apps.event.utils import generate_qr_code
from celery import shared_task


@shared_task
def send_ticket_email(tickets_data, recipient_email):
    subject = "Your Event Tickets"
    message = "Here are your tickets."

    email = EmailMessage(
        subject, message, settings.DEFAULT_FROM_EMAIL, to=recipient_email
    )

    # Loop through the tickets and generate a QR code for each
    for ticket in tickets_data:
        ticket_info = f"Ticket ID: {ticket['ticket_number']}, Seat: {ticket['seat_number']}"
        print("????", ticket_info)

        # Generate the QR code for each ticket
        qr_image = generate_qr_code(ticket_info)

        # Attach QR Code to Email
        email.attach(f"ticket_qr_{ticket['ticket_number']}.png", qr_image.getvalue(), "image/png")

    # Send the email
    email.send()
