from rest_framework.exceptions import APIException


class ServiceBaseException(APIException):
    status_code = 500
    default_detail = "An error occurred in the ticketing system"
    default_code = "TICKETING_ERROR"


class NotFoundException(APIException):
    status_code = 404
    default_detail = "Not found"
    default_code = "NOT_FOUND"


class SerializationError(APIException):
    status_code = 500
    default_detail = "Object Serialization Error"
    default_code = "SERIALIZATION_ERROR"


class DataIntegrityError(ServiceBaseException):
    status_code = 500
    default_detail = "A system error occurred"
    default_code = "DATA_INTEGRITY_ERROR"


class ExternalServiceError(ServiceBaseException):
    status_code = 502
    default_detail = "External service temporarily unavailable"
    default_code = "EXTERNAL_SERVICE_ERROR"
