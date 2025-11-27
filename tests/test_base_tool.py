"""
Tests for BaseTool
Tests shared utilities, response formatting, and error handling decorator
"""
import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'agent_tools'))

from base_tool import BaseTool


class TestBaseTool:
    """Test suite for BaseTool class"""
    
    @pytest.fixture
    def base_tool(self):
        """Create BaseTool instance for testing"""
        return BaseTool(logger_name="test_logger")
    
    def test_format_response_success(self, base_tool):
        """Test format_response with successful operation"""
        response = base_tool.format_response(
            success=True,
            data={"key": "value"},
            error=None
        )
        
        assert response["success"] is True
        assert response["data"] == {"key": "value"}
        assert response["error"] is None
    
    def test_format_response_failure(self, base_tool):
        """Test format_response with failed operation"""
        response = base_tool.format_response(
            success=False,
            data=None,
            error="Operation failed"
        )
        
        assert response["success"] is False
        assert response["data"] is None
        assert response["error"] == "Operation failed"
    
    def test_format_response_default_values(self, base_tool):
        """Test format_response with default values"""
        response = base_tool.format_response(success=True)
        
        assert response["success"] is True
        assert response["data"] is None
        assert response["error"] is None
    
    def test_error_handler_decorator_success(self, base_tool):
        """Test error_handler decorator with successful operation"""
        @base_tool.error_handler("test_operation")
        def test_function():
            return base_tool.format_response(success=True, data="success")
        
        result = test_function()
        assert result["success"] is True
        assert result["data"] == "success"
    
    def test_error_handler_decorator_exception(self, base_tool):
        """Test error_handler decorator catches exceptions"""
        @base_tool.error_handler("failing_operation")
        def failing_function():
            raise ValueError("Test error")
        
        result = failing_function()
        assert result["success"] is False
        assert "Test error" in result["error"]
        assert result["data"] is None
    
    def test_error_handler_decorator_preserves_function_name(self, base_tool):
        """Test error_handler decorator preserves original function name"""
        @base_tool.error_handler("test_op")
        def my_function():
            return base_tool.format_response(success=True)
        
        assert my_function.__name__ == "my_function"
    
    def test_logger_initialization(self):
        """Test logger initialization with custom name"""
        tool = BaseTool(logger_name="custom_logger")
        logger = tool._get_logger()
        assert logger.name == "custom_logger"
    
    def test_logger_default_name(self):
        """Test logger uses default name when not specified"""
        tool = BaseTool()
        logger = tool._get_logger()
        assert logger is not None
        assert isinstance(logger.name, str)
    
    def test_format_response_consistency(self, base_tool):
        """Test format_response always returns dict with required keys"""
        responses = [
            base_tool.format_response(True),
            base_tool.format_response(False),
            base_tool.format_response(True, data=[1, 2, 3]),
            base_tool.format_response(False, error="error message")
        ]
        
        for response in responses:
            assert isinstance(response, dict)
            assert "success" in response
            assert "data" in response
            assert "error" in response
