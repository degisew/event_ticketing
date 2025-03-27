from enum import Enum


class ReservationPaymentStatuses(Enum):
    TYPE = 'reservation_payment_status'
    PENDING = 'reservation_payment_pending'
    PAID = 'reservation_payment_paid'
    CANCELED = 'reservation_payment_canceled'
    REFUNDED = 'reservation_payment_refunded'


class ReservationStatuses(Enum):
    TYPE = 'reservation_status'
    PENDING = 'reservation_pending'
    CONFIRMED = 'reservation_confirmed'
    CANCELED = 'reservation_canceled'
    COMPLETED = 'reservation_completed'
    REFUNDED = 'reservation_refunded'


class TicketStatuses(Enum):
    TYPE = 'ticket_status'
    ACTIVE = 'ticket_status_active'
    SOLD = 'ticket_status_sold'


class TicketCategory(Enum):
    TYPE = "ticket_category_type"
    NORMAL = "ticket_category_normal"
    VIP = "ticket_category_vip"
