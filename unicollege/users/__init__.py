import logging

logger = logging.getLogger(__name__)


class GenderType:
    """ISO 5218 Base
    one-character numeric code
    """
    NOT_KNOWN = "0"
    MALE = "1"
    FEMALE = "2"
    NOT_APPLICABLE = "9"

    CHOICES = [
        (NOT_KNOWN, "Not known"),
        (MALE, "Male"),
        (FEMALE, "Female"),
        (NOT_APPLICABLE, "Not applicable")
    ]
