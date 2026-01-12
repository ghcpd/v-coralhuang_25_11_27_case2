"""
Base Tool for AI Agent
Provides shared utilities for all agent tools including error handling, 
response formatting, and logging configuration.
"""
import logging
import functools
from typing import Any, Dict, Callable


class BaseTool:
    """Base class providing common functionality for all agent tools."""
    
    def __init__(self):
        """Initialize base tool with logger."""
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @staticmethod
    def format_response(success: bool, data: Any = None, error: str = None) -> Dict[str, Any]:
        """
        Format a standardized response dictionary.
        
        Args:
            success: Whether the operation was successful
            data: The data to return (None if operation failed)
            error: Error message (None if operation succeeded)
        
        Returns:
            Standardized response dictionary with success, data, and error fields
        """
        return {
            "success": success,
            "error": error,
            "data": data
        }
    
    @staticmethod
    def handle_errors(operation_name: str = "operation") -> Callable:
        """
        Decorator for consistent error handling and logging.
        
        Args:
            operation_name: Name of the operation for logging purposes
        
        Returns:
            Decorated function with error handling
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                try:
                    self.logger.info(f"Starting {operation_name}: {func.__name__}")
                    result = func(self, *args, **kwargs)
                    self.logger.info(f"Completed {operation_name}: {func.__name__}")
                    return result
                except Exception as e:
                    error_msg = f"Error in {operation_name} ({func.__name__}): {str(e)}"
                    self.logger.error(error_msg)
                    return BaseTool.format_response(success=False, error=str(e))
            return wrapper
        return decorator
    
    def _log_operation(self, message: str, level: str = "info") -> None:
        """
        Log an operation message at the specified level.
        
        Args:
            message: Message to log
            level: Logging level (info, warning, error, debug)
        """
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(message)
