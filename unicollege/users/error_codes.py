from enum import Enum


class UserErrorCode(Enum):
    INACTIVE = "inactive"
    INVALID = "invalid"
    INVALID_PASSWORD = "invalid_password"
    NOT_FOUND = "not_found"
    REQUIRED = "required"
    UNIQUE = "unique"
