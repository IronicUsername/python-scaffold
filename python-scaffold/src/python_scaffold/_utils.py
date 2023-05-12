from enum import Enum, auto


class LOG_LEVEL(str, Enum):
    """Describe available log levels.

    Reference: https://docs.python.org/3/library/logging.html#logging-levels
    """

    CRITICAL = auto()
    ERROR = auto()
    INFO = auto()
    WARNING = auto()
    DEBUG = auto()
    NOTSET = auto()

    def __str__(self) -> str:
        """Convert enum to string."""
        return f"{self.name}"
