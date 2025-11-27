import pytest
import requests

from src.agent_tools.api_tool import APITool
from src.agent_tools.api_tool_refactored import APIToolRefactored


class FakeResponse:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json_data = json_data or {}

    def json(self):
        if isinstance(self._json_data, Exception):
            raise self._json_data
        return self._json_data


@pytest.fixture
def fake_requests(monkeypatch):
    class DummyRequests:
        def __init__(self):
            self.last_url = None
            self.last_headers = None
            self.last_params = None
            self.response = FakeResponse()

        def get(self, url, headers=None, params=None, timeout=None):
            self.last_url = url
            self.last_headers = headers
            self.last_params = params
            return self.response

    dummy = DummyRequests()
    monkeypatch.setattr(requests, "get", dummy.get)
    return dummy


@pytest.fixture
def api_tools(fake_requests):
    base_url = "https://api.example.com"
    api_key = "test-key"
    original = APITool(base_url, api_key)
    refactored = APIToolRefactored(base_url, api_key, session=fake_requests)
    return original, refactored, fake_requests


def test_fetch_weather_success(api_tools):
    original, refactored, fake_requests = api_tools
    fake_requests.response = FakeResponse(json_data={"temp": 72})

    orig_res = original.fetch_weather("Austin")
    ref_res = refactored.fetch_weather("Austin")

    assert orig_res["success"] is True
    assert ref_res["success"] is True
    assert orig_res["data"] == ref_res["data"] == {"temp": 72}


def test_fetch_news_http_error(api_tools):
    original, refactored, fake_requests = api_tools
    fake_requests.response = FakeResponse(status_code=404)

    orig_res = original.fetch_news("tech")
    ref_res = refactored.fetch_news("tech")

    assert orig_res["success"] is False
    assert ref_res["success"] is False
    assert "HTTP" in orig_res["error"]
    assert "HTTP" in ref_res["error"]


def test_fetch_stock_invalid_json(api_tools):
    original, refactored, fake_requests = api_tools
    fake_requests.response = FakeResponse(json_data=ValueError("bad json"))

    orig_res = original.fetch_stock_price("MSFT")
    ref_res = refactored.fetch_stock_price("MSFT")

    assert orig_res["success"] is False
    assert ref_res["success"] is False


def test_refactored_uses_params(api_tools):
    _, refactored, fake_requests = api_tools
    fake_requests.response = FakeResponse(json_data={"temp": 70})

    refactored.fetch_weather("Seattle")
    assert fake_requests.last_params == {"city": "Seattle"}
