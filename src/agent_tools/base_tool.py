"""
Base utilities for agent tools
"""
import functools
import logging
from typing import Any, Callable, Optional, Dict


class BaseTool:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def format_response(success: bool, data: Optional[Any] = None, error: Optional[str] = None) -> Dict[str, Any]:
        """Return a consistent response shape for tools."""
        return {"success": success, "error": error, "data": data}

    @staticmethod
    def handle_errors(func: Callable) -> Callable:
        """Decorator to wrap tool methods and return consistent responses on exceptions."""

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                # Use the tool's logger if available
                logger = getattr(self, "logger", logging.getLogger(func.__name__))
                logger.error(f"Unhandled error in {func.__name__}: {e}")
                return BaseTool.format_response(False, data=None, error=str(e))

        return wrapper


__all__ = ["BaseTool"]
