"""Main entry point for the application."""
import logging

from . import settings
from ._logging import configure_logging
from .database import setup_database

_LOGGER = logging.getLogger(__name__)


def start() -> None:
    """Start the application."""
    configure_logging(settings.log_level)
    setup_database()
    _LOGGER.info("Service started.")
