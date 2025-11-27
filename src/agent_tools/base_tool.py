"""
BaseTool provides shared utilities for agent tools, including
response formatting, logging, and a reusable error-handling decorator.
"""
import logging
from functools import wraps
from typing import Any, Callable, Dict


class BaseTool:
    """Common base for tools with shared response formatting and error handling."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.logger = logger or logging.getLogger(self.__class__.__name__)

    # We intentionally make this a staticmethod so decorators can call it
    @staticmethod
    def format_response(success: bool, data: Any = None, error: str | None = None, **extra: Any) -> Dict[str, Any]:
        response = {"success": success, "data": data, "error": error}
        response.update(extra)
        return response

    @classmethod
    def error_handler(cls, func: Callable) -> Callable:
        """
        Decorator to catch exceptions, log them, and return a standardized response.
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as exc:  # broad by design for tool boundary
                logger = getattr(self, "logger", logging.getLogger(func.__module__))
                logger.exception("Unhandled error in %s", func.__name__)
                return cls.format_response(False, data=None, error=str(exc))

        return wrapper
