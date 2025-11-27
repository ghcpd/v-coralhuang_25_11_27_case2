"""
Base Tool for AI Agent
Provides shared utilities for all tools: response formatting, error handling, and logging
"""
import logging
from functools import wraps
from typing import Dict, Any, Callable


class BaseTool:
    """Base class for all agent tools providing shared functionality"""
    
    def __init__(self, logger_name: str = None):
        """Initialize BaseTool with logger"""
        self.logger = logging.getLogger(logger_name or __name__)
    
    @staticmethod
    def format_response(success: bool, data: Any = None, error: str = None) -> Dict[str, Any]:
        """
        Format response in consistent structure
        
        Args:
            success: Whether operation was successful
            data: Response data (default None)
            error: Error message if operation failed (default None)
            
        Returns:
            Formatted response dictionary
        """
        return {
            "success": success,
            "error": error,
            "data": data
        }
    
    def error_handler(self, operation_name: str) -> Callable:
        """
        Decorator for consistent error handling across all operations
        
        Args:
            operation_name: Name of the operation for logging
            
        Returns:
            Decorated function
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    self.logger.info(f"Starting {operation_name}")
                    result = func(*args, **kwargs)
                    self.logger.info(f"Successfully completed {operation_name}")
                    return result
                except Exception as e:
                    self.logger.error(f"Error in {operation_name}: {str(e)}")
                    return self.format_response(
                        success=False,
                        error=str(e),
                        data=None
                    )
            return wrapper
        return decorator
    
    def _get_logger(self) -> logging.Logger:
        """Get logger instance"""
        return self.logger
