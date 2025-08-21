import aiohttp
import pytest
from unittest.mock import patch

from mcpturbo_core.messages import Request
from mcpturbo_core.protocol import send_external_request

pytestmark = pytest.mark.asyncio


class DummyAgent:
    api_url = "https://api.example.com"
    api_key = "test"


class MockResponse:
    def __init__(self, status: int, json_data=None, text_data="error"):
        self.status = status
        self._json = json_data or {}
        self._text = text_data

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def json(self):
        return self._json

    async def text(self):
        return self._text


async def test_send_external_request_retries_on_500():
    agent = DummyAgent()
    request = Request(sender="s", target="t", action="a")

    responses = [
        MockResponse(500),
        MockResponse(500),
        MockResponse(200, json_data={"ok": True}),
    ]

    def mock_post(*args, **kwargs):
        return responses.pop(0)

    async with aiohttp.ClientSession() as session:
        with patch.object(session, "post", side_effect=mock_post) as post:
            result = await send_external_request(session, agent, request)
            assert result == {"ok": True}
            assert post.call_count == 3
