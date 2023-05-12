"""Test for the database connector module."""
from sqlalchemy import select
from sqlalchemy.orm import Session


def test_db_connection(db_session: Session) -> None:
    """Test db connection."""
    res = db_session.scalar(select(1))
    assert res == 1
