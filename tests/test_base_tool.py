import pytest
from src.agent_tools.base_tool import BaseTool


class DummyTool(BaseTool):
    @BaseTool.handle_errors
    def will_raise(self):
        raise RuntimeError("boom")


def test_format_response():
    r = BaseTool.format_response(True, data={"a": 1}, error=None)
    assert r == {"success": True, "error": None, "data": {"a": 1}}


def test_handle_errors_decorator_returns_error_shape():
    t = DummyTool()
    r = t.will_raise()
    assert isinstance(r, dict)
    assert r["success"] is False
    assert r["data"] is None
    assert isinstance(r["error"], str) and "boom" in r["error"]
