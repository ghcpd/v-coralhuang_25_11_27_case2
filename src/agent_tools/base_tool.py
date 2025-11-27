"""
Base utilities for agent tools
Provides response formatting and a decorator for centralized error handling
"""
import functools
import logging
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger(__name__)


def handle_errors(func: Callable) -> Callable:
    """Decorator to centralize error handling for tools

    The decorated function must return a dict with the key `data` when
    there's a successful result. This decorator ensures a consistent
    response shape: {"success": bool, "error": Optional[str], "data": Any}
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:  # catch all to keep API stable
            logger.exception("Unhandled exception in tool")
            return {"success": False, "error": str(exc), "data": None}

    return wrapper


class BaseTool:
    """Shared utilities for agent tools

    Keeps response formatting and common helpers centralized so each tool
    can focus on business logic, not repetitive response handling.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def format_response(success: bool, error: Optional[str], data: Any) -> Dict[str, Any]:
        return {"success": success, "error": error, "data": data}
