"""
Tests for APIToolRefactored
Tests generic request execution, unified error handling, and centralized headers
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import requests
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'agent_tools'))

from api_tool_refactored import APIToolRefactored
from api_tool import APITool


class TestAPIToolRefactored:
    """Test suite for APIToolRefactored class"""
    
    @pytest.fixture
    def api_tool_refactored(self):
        """Create APIToolRefactored instance for testing"""
        return APIToolRefactored(
            base_url="https://api.example.com",
            api_key="test_key_12345"
        )
    
    @pytest.fixture
    def api_tool_original(self):
        """Create original APITool instance for comparison"""
        return APITool(
            base_url="https://api.example.com",
            api_key="test_key_12345"
        )
    
    def test_get_headers_structure(self, api_tool_refactored):
        """Test _get_headers returns correct structure"""
        headers = api_tool_refactored._get_headers()
        
        assert isinstance(headers, dict)
        assert "Authorization" in headers
        assert "Content-Type" in headers
        assert headers["Authorization"] == "Bearer test_key_12345"
        assert headers["Content-Type"] == "application/json"
    
    def test_get_headers_consistency(self, api_tool_refactored):
        """Test _get_headers returns consistent values"""
        headers1 = api_tool_refactored._get_headers()
        headers2 = api_tool_refactored._get_headers()
        
        assert headers1 == headers2
    
    @pytest.mark.parametrize("endpoint_type,param_value", [
        ("weather", "New York"),
        ("news", "technology"),
        ("stock", "AAPL")
    ])
    def test_make_request_all_endpoints(self, api_tool_refactored, endpoint_type, param_value):
        """Test generic _make_request with all endpoint types"""
        with patch.object(api_tool_refactored, '_make_http_request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"data": "test"}
            mock_request.return_value = mock_response
            
            result = api_tool_refactored._make_request(endpoint_type, param_value)
            
            assert result["success"] is True
            assert result["error"] is None
            assert result["data"] == {"data": "test"}
    
    def test_fetch_weather_success(self, api_tool_refactored):
        """Test successful weather fetch"""
        with patch.object(api_tool_refactored, '_make_http_request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"temp": 72, "condition": "sunny"}
            mock_request.return_value = mock_response
            
            result = api_tool_refactored.fetch_weather("New York")
            
            assert result["success"] is True
            assert result["error"] is None
            assert result["data"]["temp"] == 72
    
    def test_fetch_news_success(self, api_tool_refactored):
        """Test successful news fetch"""
        with patch.object(api_tool_refactored, '_make_http_request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"articles": []}
            mock_request.return_value = mock_response
            
            result = api_tool_refactored.fetch_news("technology")
            
            assert result["success"] is True
            assert result["error"] is None
    
    def test_fetch_stock_price_success(self, api_tool_refactored):
        """Test successful stock price fetch"""
        with patch.object(api_tool_refactored, '_make_http_request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"price": 150.25}
            mock_request.return_value = mock_response
            
            result = api_tool_refactored.fetch_stock_price("AAPL")
            
            assert result["success"] is True
            assert result["error"] is None
            assert result["data"]["price"] == 150.25
    
    def test_make_request_http_error(self, api_tool_refactored):
        """Test _make_request handles HTTP errors"""
        with patch.object(api_tool_refactored, '_make_http_request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_request.return_value = mock_response
            
            result = api_tool_refactored._make_request("weather", "Unknown City")
            
            assert result["success"] is False
            assert "HTTP 404" in result["error"]
            assert result["data"] is None
    
    def test_make_request_timeout_error(self, api_tool_refactored):
        """Test _make_request handles timeout errors"""
        with patch.object(api_tool_refactored, '_make_http_request') as mock_request:
            mock_request.side_effect = requests.Timeout()
            
            result = api_tool_refactored._make_request("weather", "New York")
            
            assert result["success"] is False
            assert "timeout" in result["error"].lower()
            assert result["data"] is None
    
    def test_make_request_generic_exception(self, api_tool_refactored):
        """Test _make_request handles generic exceptions"""
        with patch.object(api_tool_refactored, '_make_http_request') as mock_request:
            mock_request.side_effect = Exception("Network error")
            
            result = api_tool_refactored._make_request("weather", "New York")
            
            assert result["success"] is False
            assert "Network error" in result["error"]
            assert result["data"] is None
    
    def test_make_request_invalid_endpoint(self, api_tool_refactored):
        """Test _make_request with invalid endpoint type"""
        result = api_tool_refactored._make_request("invalid", "value")
        
        assert result["success"] is False
        assert "Unknown endpoint type" in result["error"]
        assert result["data"] is None
    
    def test_endpoint_config_completeness(self, api_tool_refactored):
        """Test that ENDPOINT_CONFIG has all required endpoints"""
        required_endpoints = ["weather", "news", "stock"]
        for endpoint in required_endpoints:
            assert endpoint in api_tool_refactored.ENDPOINT_CONFIG
            config = api_tool_refactored.ENDPOINT_CONFIG[endpoint]
            assert "path" in config
            assert "params_key" in config
    
    def test_request_url_construction(self, api_tool_refactored):
        """Test that request URLs are constructed correctly"""
        with patch.object(api_tool_refactored, '_make_http_request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {}
            mock_request.return_value = mock_response
            
            api_tool_refactored.fetch_weather("New York")
            
            # Verify URL was constructed correctly
            call_args = mock_request.call_args
            url = call_args[0][0]
            assert "weather" in url
            assert "city=New York" in url
    
    def test_headers_passed_to_request(self, api_tool_refactored):
        """Test that headers are correctly passed to HTTP request"""
        with patch.object(api_tool_refactored, '_make_http_request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {}
            mock_request.return_value = mock_response
            
            api_tool_refactored.fetch_weather("New York")
            
            # Verify headers were passed
            call_args = mock_request.call_args
            headers = call_args[0][1]
            assert headers["Authorization"] == "Bearer test_key_12345"
            assert headers["Content-Type"] == "application/json"
    
    def test_comparison_original_vs_refactored_structure(self, api_tool_original, api_tool_refactored):
        """Test that refactored tool returns same structure as original"""
        with patch.object(api_tool_refactored, '_make_http_request') as mock_refactored:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"data": "test"}
            mock_refactored.return_value = mock_response
            
            original_result = api_tool_original.fetch_weather("Test")
            refactored_result = api_tool_refactored.fetch_weather("Test")
            
            # Both should have same top-level structure
            assert set(original_result.keys()) == set(refactored_result.keys())
    
    def test_timeout_constant_used(self, api_tool_refactored):
        """Test that DEFAULT_TIMEOUT constant is used"""
        assert api_tool_refactored.DEFAULT_TIMEOUT == 10
    
    def test_make_http_request_wrapper(self, api_tool_refactored):
        """Test _make_http_request wrapper for mocking support"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_get.return_value = mock_response
            
            response = api_tool_refactored._make_http_request(
                "https://api.example.com/test",
                {"Authorization": "Bearer test"}
            )
            
            assert response.status_code == 200
            mock_get.assert_called_once()
