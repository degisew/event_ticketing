import qrcode
from io import BytesIO


def generate_qr_code(ticket_info: str):
    """Generate a QR code from ticket info and return it as an in-memory file."""
    qr = qrcode.make(ticket_info)
    img_io = BytesIO()
    qr.save(img_io, format="PNG")
    img_io.seek(0)
    return img_io  # This can be used as an email attachment
