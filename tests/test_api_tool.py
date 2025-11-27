import pytest
from unittest.mock import patch, Mock

from src.agent_tools.api_tool_refactored import APIToolRefactored
from src.agent_tools.api_tool import APITool as OrigAPITool


@pytest.fixture
def api_tool():
    return APIToolRefactored("https://api.example.com", "secret")


def _fake_response(status=200, json_data=None):
    mock = Mock()
    mock.status_code = status
    mock.json = Mock(return_value=json_data or {"ok": True})
    return mock


def test_fetch_weather_success(api_tool):
    with patch("requests.get", return_value=_fake_response(200, {"temp": 20})) as mock_get:
        result = api_tool.fetch_weather("London")
        assert result["success"] is True
        assert result["data"]["temp"] == 20
        mock_get.assert_called_once()


def test_fetch_news_http_error(api_tool):
    with patch("requests.get", return_value=_fake_response(500)):
        result = api_tool.fetch_news("tech")
        assert result["success"] is False
        assert "HTTP 500" in result["error"]


def test_refactored_matches_original(monkeypatch):
    orig = OrigAPITool("https://api.example.com", "secret")
    ref = APIToolRefactored("https://api.example.com", "secret")
    with patch("requests.get", return_value=_fake_response(200, {"x": 1})):
        a = orig.fetch_weather("London")
        b = ref.fetch_weather("London")
        assert a["success"] == b["success"]
        assert a["data"] == b["data"]
