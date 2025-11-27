import logging

import pytest

from src.agent_tools.base_tool import BaseTool


def test_format_response_success():
    resp = BaseTool.format_response(True, data={"ok": 1})
    assert resp == {"success": True, "data": {"ok": 1}, "error": None}


def test_format_response_error_with_extra():
    resp = BaseTool.format_response(False, data=None, error="boom", details="x")
    assert resp["success"] is False
    assert resp["error"] == "boom"
    assert resp["details"] == "x"


def test_error_handler_catches_exceptions(caplog):
    class Dummy(BaseTool):
        @BaseTool.error_handler
        def do_fail(self):
            raise ValueError("fail")

    d = Dummy()
    with caplog.at_level(logging.ERROR):
        resp = d.do_fail()
    assert resp["success"] is False
    assert resp["error"] == "fail"


def test_error_handler_passthrough_success():
    class Dummy(BaseTool):
        @BaseTool.error_handler
        def do_ok(self):
            return BaseTool.format_response(True, data=123)

    d = Dummy()
    resp = d.do_ok()
    assert resp == {"success": True, "data": 123, "error": None}
