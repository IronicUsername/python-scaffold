"""Test for the database crud functions."""
from typing import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from python_scaffold.database.models import ExampleTable


def test_functionality_execution_table(
    db_session: Session, insert_row_example_table: Callable[..., list[ExampleTable]]
) -> None:
    """Test if a `ExampleTable` entity was created correctly in the db."""
    sample_data = insert_row_example_table(db_session)
    data_in_db = db_session.scalars(select(ExampleTable)).all()
    assert data_in_db == sample_data
