import pytest
from unittest.mock import patch

import requests

from src.agent_tools.api_tool import APITool as OriginalAPI
from src.agent_tools.api_tool_refactored import APIToolRefactored


class FakeResponse:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self._payload = payload or {"ok": True}

    def json(self):
        return self._payload


@pytest.fixture
def orig_api():
    return OriginalAPI("https://api.example.com", "key123")


@pytest.fixture
def ref_api():
    return APIToolRefactored("https://api.example.com", "key123")


def test_make_request_success(ref_api):
    fake = FakeResponse(200, {"temp": 20})

    with patch("requests.get", return_value=fake) as mock_get:
        res = ref_api.fetch_weather("Seattle")
        assert res["success"] is True
        assert res["data"] == {"temp": 20}
        mock_get.assert_called_once()


def test_request_non_200_handled(ref_api):
    fake = FakeResponse(500, {"error": "boom"})
    with patch("requests.get", return_value=fake):
        res = ref_api.fetch_news("sports")
        assert res["success"] is False
        assert "HTTP 500" in res["error"]


def test_original_and_refactored_output_match(orig_api, ref_api):
    fake = FakeResponse(200, {"value": 1})

    with patch("requests.get", return_value=fake):
        orig_res = orig_api.fetch_stock_price("MSFT")
        ref_res = ref_api.fetch_stock_price("MSFT")

    assert orig_res["success"] == ref_res["success"]
    assert orig_res["data"] == ref_res["data"]
