import pytest

from src.agent_tools.base_tool import BaseTool


def test_format_response():
    r = BaseTool.format_response(True, None, data=[1])
    assert r == {"success": True, "error": None, "data": [1]}


def test_error_handler_decorator_logs_and_handles_exception(monkeypatch):
    class Fake(BaseTool):
        def __init__(self):
            super().__init__()

        @BaseTool.error_handler
        def will_raise(self):
            raise ValueError("boom")

    f = Fake()
    res = f.will_raise()
    assert res["success"] is False
    assert "boom" in res["error"]
