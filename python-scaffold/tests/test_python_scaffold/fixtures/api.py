"""API related fixtures."""
from contextlib import contextmanager
from typing import Any, Callable, ContextManager, Generator
from uuid import uuid4

import pytest
import respx
from fastapi.testclient import TestClient
from httpx import Request, Response

from python_scaffold import api, settings


@pytest.fixture(scope="session")
def test_client() -> TestClient:
    """Test client of the service.

    [Read here for more](https://fastapi.tiangolo.com/tutorial/testing/)
    """
    return TestClient(api.app)


@pytest.fixture()
def mock_api_auth() -> Callable[[Response | None], ContextManager[dict[str, respx.Route]]]:
    """Mock API for the auth API."""

    @contextmanager
    def _mock_api_auth(custom_response: Response | None = None) -> Generator[dict[str, respx.Route], None, None]:
        def _dynamic_message_response(request: Request) -> Response:
            if custom_response:
                return custom_response
            return Response(201, json={"access_token": uuid4().hex})

        route_auth = respx.post(url=settings.external_api_auth_url, name="auth").mock(
            side_effect=_dynamic_message_response
        )
        yield {"auth": route_auth}

    return _mock_api_auth


@pytest.fixture()
def example_message() -> str:
    """Just a simple example message."""
    return "Hi i am a example message."


@pytest.fixture()
async def mock_api_messages(example_message: str) -> Callable[..., ContextManager[dict[str, respx.Route]]]:
    """Mock an external API."""

    @contextmanager
    def _mock_api_messages(
        messages: list[dict[str, Any]] | None = None
    ) -> Generator[dict[str, respx.Route], None, None]:
        _default_messageid = "0" * 8

        def _dynamic_message_response(request: Request) -> Response:
            request_url_id = str(request.url).split("/")[-1]

            if not request_url_id:
                return Response(403, json={"details": "Error in request: no ID was given"})

            message = example_message
            if len(messages_ids_to_respond_custom_msg):
                message = [
                    msg.get("base_message", example_message)
                    for msg in messages_ids_to_respond_custom_msg
                    if msg.get("messageid", _default_messageid) == request_url_id
                ][0]

            if not len(message):
                return Response(404, json={"details": "Error in request: no MSCONS with this ID exists."})
            return Response(200, json=[{"edifact": message}])

        messages_ids_to_respond_custom_msg = (
            [message for message in messages if bool(message["compacted"])] if messages else []
        )
        route_messages = respx.get(
            url=settings.external_api_base_url, path__startswith="/", name="get_some_messages"
        ).mock(side_effect=_dynamic_message_response)
        yield {"messages": route_messages}

    return _mock_api_messages
