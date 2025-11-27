import pytest

from src.agent_tools.base_tool import BaseTool, handle_errors


class DummyTool(BaseTool):
    @handle_errors
    def raise_error(self):
        raise RuntimeError("boom")


def test_format_response():
    res = BaseTool.format_response(True, None, {"a": 1})
    assert res["success"] is True
    assert res["error"] is None
    assert res["data"] == {"a": 1}


def test_handle_errors_decorator():
    t = DummyTool()
    res = t.raise_error()
    assert res["success"] is False
    assert "boom" in res["error"]
    assert res["data"] is None
