"""
Base shared utilities for agent tools
- format_response(): creates consistent dict
- error_handler decorator: wraps methods and converts exceptions into responses
- logger helper
"""
import functools
import logging
from typing import Any, Callable, Optional


class BaseTool:
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(self.__class__.__name__)

    @staticmethod
    def format_response(success: bool, error: Optional[str] = None, data: Any = None) -> dict:
        return {"success": success, "error": error, "data": data}

    @staticmethod
    def error_handler(func: Callable):
        """Decorator to convert exceptions to a standard response dict"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:  # catch-all ensures uniform handling
                # If instance has logger, log the error
                instance = args[0] if args else None
                if instance and hasattr(instance, "logger"):
                    instance.logger.error(f"Error in {func.__name__}: {exc}")
                return BaseTool.format_response(False, error=str(exc), data=None)

        return wrapper


__all__ = ["BaseTool"]
