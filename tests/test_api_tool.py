import pytest
from unittest.mock import patch

from src.agent_tools.api_tool import APITool as LegacyAPI
from src.agent_tools.api_tool_refactored import APIToolRefactored


class DummyResponse:
    def __init__(self, status_code=200, data=None, text=""):
        self.status_code = status_code
        self._data = data or {"ok": True}
        self.text = text

    def json(self):
        return self._data


@pytest.fixture
def legacy_api():
    return LegacyAPI("https://api.test", "KEY")


@pytest.fixture
def refactored_api():
    def request_fn(url, headers=None, params=None, timeout=None):
        return DummyResponse(200, {"url": url, "params": params})

    return APIToolRefactored("https://api.test", "KEY", request_fn=request_fn)


def test_fetch_weather_matches_legacy(legacy_api, refactored_api):
    dummy = DummyResponse(200, {"temp": 20})
    with patch("src.agent_tools.api_tool.requests.get", return_value=dummy):
        legacy_res = legacy_api.fetch_weather("London")
    # ensure refactored uses the same response shape as patched legacy
    refactored_api._request_fn = lambda url, headers=None, params=None, timeout=None: DummyResponse(200, {"temp": 20})
    refactored_res = refactored_api.fetch_weather("London")
    assert legacy_res["success"] == refactored_res["success"]
    assert legacy_res["data"] == refactored_res["data"]


@pytest.mark.parametrize("method,args", [
    ("fetch_weather", ("London",)),
    ("fetch_news", ("tech",)),
    ("fetch_stock_price", ("AAPL",)),
])
def test_api_methods_success(refactored_api, method, args):
    fn = getattr(refactored_api, method)
    res = fn(*args)
    assert res["success"] is True
    assert res["data"] is not None
