"""Utility functions for the database logic."""
import logging

from sqlalchemy.schema import CreateSchema

from .. import settings
from . import connectors as database_connectors
from .models import Base as DatabaseTableBase

_LOGGER = logging.getLogger(__name__)


def setup_database() -> None:
    """Create database schemas and tables if existent."""
    _LOGGER.info("Connecting to database.")
    with database_connectors.get_database_session(database_dsn=settings.database_dsn) as session:
        engine = session.get_bind()
        with engine.connect() as connection:
            with connection.begin():
                if not connection.dialect.has_schema(  # type: ignore # "Dialect" has no attribute "has_schema"
                    connection,
                    DatabaseTableBase.metadata.schema,
                ):
                    connection.execute(CreateSchema(DatabaseTableBase.metadata.schema))
                    _LOGGER.info(f"Schema {DatabaseTableBase.metadata.schema} successfully created.")
                else:
                    _LOGGER.warn(f"Schema {DatabaseTableBase.metadata.schema} already exists.")
        DatabaseTableBase.metadata.create_all(engine)
