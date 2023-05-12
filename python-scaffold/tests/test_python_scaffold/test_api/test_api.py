from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_healthcheck_successful(test_client: TestClient) -> None:
    message_count = test_client.get("/healthcheck")

    assert message_count.status_code == 200
    assert message_count.json() == {"is_healthy": True}


def test_healthcheck_database_successful(test_client: TestClient, db_session: Session) -> None:
    message_count = test_client.get("/healthcheck-database")

    assert message_count.status_code == 200
    assert message_count.json() == {"is_healthy": True}
