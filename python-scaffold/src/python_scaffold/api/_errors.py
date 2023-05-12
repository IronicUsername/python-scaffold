"""Module to structure custom errors."""


class BaseExceptionConfig(Exception):
    """Describe the base functionality for the custom errors."""

    def __init__(self, *args) -> None:  # type: ignore[no-untyped-def]
        self.message = None
        if args:
            self.message = args[0]

    def __str__(self) -> str:
        """Generate a default error message."""
        if self.message:
            return f"{self.__class__.__name__}, {self.message} "
        return "{self.__class__.__name__}, Custom error occurred."


class DatabaseConnectionError(BaseException):
    """Describe a custom error for a weird error that should actually never happen."""
