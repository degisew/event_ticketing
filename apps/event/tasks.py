from django.conf import settings
from django.core.mail import EmailMessage
from apps.event.utils import generate_qr_code
from celery import shared_task


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
