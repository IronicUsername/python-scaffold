"""Database related test fixtures."""
from contextlib import contextmanager
from typing import Any, Callable, ContextManager, Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.schema import CreateSchema, DropSchema

from python_scaffold import database, settings


@pytest.fixture(scope="session")
def engine() -> Any:
    """Create db engine to build a db connection."""
    return create_engine(settings.database_dsn, isolation_level="REPEATABLE READ", future=True)


@pytest.fixture(scope="session")
def session_provider(engine: Any) -> Callable[[], ContextManager[Session]]:
    """Db session provider."""

    @contextmanager
    def _get_session() -> Iterator[Session]:
        try:
            database.models.Base.metadata.drop_all(engine)
        except Exception:  # noqa: B902
            pytest.fail("No database available.")

        with engine.connect() as connection:
            with connection.begin():
                if connection.dialect.has_schema(connection, database.models.Base.metadata.schema):
                    connection.execute(DropSchema(database.models.Base.metadata.schema))

                if not connection.dialect.has_schema(connection, database.models.Base.metadata.schema):
                    connection.execute(CreateSchema(database.models.Base.metadata.schema))
        database.models.Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine, future=True)
        with Session() as session:
            yield session

        database.models.Base.metadata.drop_all(engine)

    return _get_session


@pytest.fixture()
def db_session(session_provider: Callable[[], ContextManager[Session]]) -> Iterator[Session]:
    """Create a db session."""
    with session_provider() as session:
        yield session


@pytest.fixture()
def default_sample_example_table_dict() -> dict[str, Any]:
    """Return default request collector data in dict format.

    NOTE: This data still lacks id, but that will be generated on creation.
    """
    return {"text": "some_example_text"}


@pytest.fixture()
def default_sample_example_table(default_sample_example_table_dict: dict[str, Any]) -> database.models.ExampleTable:
    """Sample object of `example_table`."""
    return database.models.ExampleTable(**default_sample_example_table_dict)


@pytest.fixture()
def insert_row_example_table(
    default_sample_example_table: database.models.ExampleTable,
) -> Callable[..., list[database.models.ExampleTable]]:
    """Insert default data for ROLE model."""

    def _insert_data(
        session: Session, batch: list[database.models.ExampleTable] | None = None
    ) -> list[database.models.ExampleTable]:
        if not batch:
            batch = [default_sample_example_table]

        session.add_all(batch)
        session.commit()
        return batch

    return _insert_data
