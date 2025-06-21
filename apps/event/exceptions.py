from rest_framework.exceptions import APIException


class TicketingBaseException(APIException):
    status_code = 500
    default_detail = "An error occurred in the ticketing system"
    default_code = "TICKETING_ERROR"


class SerializationError(APIException):
    status_code = 500
    default_detail = "Object Serialization Error"
    default_code = "SERIALIZATION_ERROR"


class BusinessLogicError(TicketingBaseException):
    status_code = 400
    default_detail = "Business logic error"
    default_code = "BUSINESS_LOGIC_ERROR"


class NotEnoughSeatsAvailableError(BusinessLogicError):
    status_code = 409
    default_detail = "Not enough seats available"
    default_code = "INSUFFICIENT_SEATS"


class ReservationLimitExceededError(BusinessLogicError):
    status_code = 403
    default_detail = "Reservation limit exceeded"
    default_code = "RESERVATION_LIMIT_EXCEEDED"


class InvalidTicketTypeError(BusinessLogicError):
    status_code = 400
    default_detail = "Invalid ticket type"
    default_code = "INVALID_TICKET_TYPE"


class EventNotAvailableError(BusinessLogicError):
    status_code = 410
    default_detail = "Event is not available for reservation"
    default_code = "EVENT_NOT_AVAILABLE"


class DataIntegrityError(TicketingBaseException):
    status_code = 500
    default_detail = "A system error occurred"
    default_code = "DATA_INTEGRITY_ERROR"


class ExternalServiceError(TicketingBaseException):
    status_code = 502
    default_detail = "External service temporarily unavailable"
    default_code = "EXTERNAL_SERVICE_ERROR"


class ReservationNotFoundError(TicketingBaseException):
    status_code = 404
    default_detail = "Reservation not found"
    default_code = "RESERVATION_NOT_FOUND"


class ReservationAlreadyCancelledError(BusinessLogicError):
    status_code = 409
    default_detail = "Reservation is already cancelled"
    default_code = "RESERVATION_ALREADY_CANCELLED"


class ReservationExpiredError(BusinessLogicError):
    status_code = 410
    default_detail = "Reservation has expired"
    default_code = "RESERVATION_EXPIRED"
