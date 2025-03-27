import enum


class RoleCode(enum.Enum):

    ADMIN = "admin"
    VENDOR = "vendor"


class AccountState(enum.Enum):
    TYPE = "account_state_type"

    ACTIVE = "active"
    INACTIVE = "inactive"
