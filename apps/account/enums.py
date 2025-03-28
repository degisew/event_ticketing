import enum


class RoleCode(enum.Enum):

    ADMIN = "admin"
    USER = "user"
    ORGANIZER = "organizer"


class AccountState(enum.Enum):
    TYPE = "account_state_type"

    ACTIVE = "active"
    INACTIVE = "inactive"
