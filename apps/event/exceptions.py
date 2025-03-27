from rest_framework.exceptions import APIException


class NotEnoughSeatsAvailableError(APIException):
    status_code = 400
    default_detail = "Not enough seats available."
    default_code = "not_enough_seats_available"
