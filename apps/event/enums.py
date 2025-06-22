from enum import Enum


class ReservationPaymentStatuses(Enum):
    PENDING = "reservation_payment_pending"
    PAID = "reservation_payment_paid"
    CANCELED = "reservation_payment_canceled"
    REFUNDED = "reservation_payment_refunded"


class ReservationStatuses(Enum):
    PENDING = "reservation_pending"
    CONFIRMED = "reservation_confirmed"
    CANCELED = "reservation_canceled"
    COMPLETED = "reservation_completed"
    REFUNDED = "reservation_refunded"


class TicketStatuses(Enum):
    ACTIVE = "ticket_status_active"
    SOLD = "ticket_status_sold"


class TicketTypes(Enum):
    NORMAL = "ticket_category_normal"
    VIP = "ticket_category_vip"


# Types

RESERVATION_PAYMENT_STATUS_TYPE = "reservation_payment_status"

RESERVATION_STATUS_TYPE = "reservation_status"

TICKET_STATUS_TYPE = "ticket_status"

TICKET_TYPE = "ticket_type"
