"""Module to maintain database connection, setup, helpers."""
from contextlib import contextmanager
from typing import Any, Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .. import settings

_SESSIONMAKER = None


@contextmanager
def get_database_session(database_dsn: str) -> Iterator[Session]:
    """Get postgres_db session."""
    global _SESSIONMAKER
    if _SESSIONMAKER is None:
        connect_args: dict[str, Any] = {
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
        }
        engine = create_engine(
            database_dsn,
            isolation_level="REPEATABLE READ",
            future=True,
            connect_args=connect_args,
            pool_pre_ping=True,
            pool_recycle=300,
        )
        _SESSIONMAKER = sessionmaker(bind=engine, future=True)

    with _SESSIONMAKER() as session:
        yield session


def database_session() -> Iterator[Session]:
    """Establish a db connection with FastAPI as an dependency."""
    with get_database_session(database_dsn=settings.database_dsn) as session:
        yield session
