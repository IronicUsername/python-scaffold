import logging

from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from ._errors import DatabaseConnectionError

_LOGGER = logging.getLogger(__name__)


def healthcheck() -> dict[str, bool]:
    """Return successfully, if the API is up and running."""
    _LOGGER.info("API healthcheck successful.")
    return {"is_healthy": True}


def healthcheck_database(session: Session) -> dict[str, bool]:
    """Return successfully, if the database can be reached."""
    try:
        session.scalar(select(1))
        _LOGGER.info("Database healthcheck successful.")
        return {"is_healthy": True}
    except OperationalError as error:
        raise DatabaseConnectionError("Database connection failed.") from error
