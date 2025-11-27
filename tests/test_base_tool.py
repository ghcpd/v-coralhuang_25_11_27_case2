"""
Unit tests for BaseTool class.
Tests shared utilities including response formatting and error handling.
"""
import pytest
import logging
from src.agent_tools.base_tool import BaseTool


class TestBaseTool:
    """Test suite for BaseTool base class."""
    
    @pytest.fixture
    def base_tool(self):
        """Create a BaseTool instance for testing."""
        return BaseTool()
    
    def test_format_response_success(self):
        """Test format_response with successful operation."""
        result = BaseTool.format_response(success=True, data={"test": "data"})
        
        assert result["success"] is True
        assert result["data"] == {"test": "data"}
        assert result["error"] is None
    
    def test_format_response_failure(self):
        """Test format_response with failed operation."""
        result = BaseTool.format_response(success=False, error="Test error")
        
        assert result["success"] is False
        assert result["data"] is None
        assert result["error"] == "Test error"
    
    def test_format_response_keys(self):
        """Test that format_response always returns correct keys."""
        result = BaseTool.format_response(success=True)
        
        assert "success" in result
        assert "data" in result
        assert "error" in result
    
    def test_handle_errors_decorator_success(self, base_tool):
        """Test error handling decorator with successful function."""
        @BaseTool.handle_errors("test operation")
        def successful_function(self):
            return BaseTool.format_response(success=True, data="result")
        
        result = successful_function(base_tool)
        assert result["success"] is True
        assert result["data"] == "result"
    
    def test_handle_errors_decorator_exception(self, base_tool):
        """Test error handling decorator catches exceptions."""
        @BaseTool.handle_errors("test operation")
        def failing_function(self):
            raise ValueError("Test error")
        
        result = failing_function(base_tool)
        assert result["success"] is False
        assert "Test error" in result["error"]
    
    def test_log_operation_info(self, base_tool, caplog):
        """Test logging at info level."""
        with caplog.at_level(logging.INFO):
            base_tool._log_operation("Test info message", "info")
        
        assert "Test info message" in caplog.text
    
    def test_log_operation_error(self, base_tool, caplog):
        """Test logging at error level."""
        with caplog.at_level(logging.ERROR):
            base_tool._log_operation("Test error message", "error")
        
        assert "Test error message" in caplog.text
    
    def test_logger_initialization(self, base_tool):
        """Test that logger is properly initialized."""
        assert hasattr(base_tool, "logger")
        assert isinstance(base_tool.logger, logging.Logger)
        assert base_tool.logger.name == "BaseTool"
