"""
Unit tests for APIToolRefactored class.
Tests API operations, request handling, and comparison with original.
"""
import pytest
import requests
from unittest.mock import patch, MagicMock
from src.agent_tools.api_tool import APITool
from src.agent_tools.api_tool_refactored import APIToolRefactored


class TestAPIToolRefactored:
    """Test suite for refactored API tool."""
    
    @pytest.fixture
    def api_tool(self):
        """Create an APIToolRefactored instance for testing."""
        return APIToolRefactored("https://api.example.com", "test_api_key")
    
    @pytest.fixture
    def original_api_tool(self):
        """Create original APITool instance for comparison tests."""
        return APITool("https://api.example.com", "test_api_key")
    
    def test_initialization(self, api_tool):
        """Test API tool initialization."""
        assert api_tool.base_url == "https://api.example.com"
        assert api_tool.api_key == "test_api_key"
        assert hasattr(api_tool, "logger")
    
    def test_get_headers(self, api_tool):
        """Test header generation."""
        headers = api_tool._get_headers()
        
        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer test_api_key"
        assert headers["Content-Type"] == "application/json"
    
    @patch('src.agent_tools.api_tool_refactored.requests.get')
    def test_fetch_weather_success(self, mock_get, api_tool):
        """Test successful weather API call."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"temperature": 72, "condition": "sunny"}
        mock_get.return_value = mock_response
        
        result = api_tool.fetch_weather("New York")
        
        assert result["success"] is True
        assert result["error"] is None
        assert result["data"]["temperature"] == 72
        assert result["data"]["condition"] == "sunny"
        
        # Verify request was made with correct parameters
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "New York" in call_args[0][0] or "New York" in str(call_args)
    
    @patch('src.agent_tools.api_tool_refactored.requests.get')
    def test_fetch_news_success(self, mock_get, api_tool):
        """Test successful news API call."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"articles": [{"title": "Test News"}]}
        mock_get.return_value = mock_response
        
        result = api_tool.fetch_news("technology")
        
        assert result["success"] is True
        assert "articles" in result["data"]
    
    @patch('src.agent_tools.api_tool_refactored.requests.get')
    def test_fetch_stock_price_success(self, mock_get, api_tool):
        """Test successful stock price API call."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"symbol": "AAPL", "price": 150.25}
        mock_get.return_value = mock_response
        
        result = api_tool.fetch_stock_price("AAPL")
        
        assert result["success"] is True
        assert result["data"]["symbol"] == "AAPL"
        assert result["data"]["price"] == 150.25
    
    @patch('src.agent_tools.api_tool_refactored.requests.get')
    def test_http_error_handling(self, mock_get, api_tool):
        """Test handling of HTTP error responses."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = api_tool.fetch_weather("InvalidCity")
        
        assert result["success"] is False
        assert "404" in result["error"]
    
    @patch('src.agent_tools.api_tool_refactored.requests.get')
    def test_timeout_handling(self, mock_get, api_tool):
        """Test handling of request timeout."""
        mock_get.side_effect = requests.Timeout("Connection timeout")
        
        result = api_tool.fetch_weather("New York")
        
        assert result["success"] is False
        assert "timeout" in result["error"].lower()
    
    @patch('src.agent_tools.api_tool_refactored.requests.get')
    def test_request_exception_handling(self, mock_get, api_tool):
        """Test handling of general request exceptions."""
        mock_get.side_effect = requests.RequestException("Network error")
        
        result = api_tool.fetch_news("sports")
        
        assert result["success"] is False
        assert "Network error" in result["error"]
    
    @patch('src.agent_tools.api_tool_refactored.requests.get')
    def test_json_parsing_error(self, mock_get, api_tool):
        """Test handling of invalid JSON responses."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        
        result = api_tool.fetch_stock_price("AAPL")
        
        assert result["success"] is False
        assert "JSON" in result["error"]
    
    @pytest.mark.parametrize("method,param", [
        ("fetch_weather", "Boston"),
        ("fetch_news", "business"),
        ("fetch_stock_price", "GOOGL"),
    ])
    @patch('src.agent_tools.api_tool_refactored.requests.get')
    def test_all_methods_use_generic_request(self, mock_get, api_tool, method, param):
        """Test that all public methods use the generic _make_request method."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success"}
        mock_get.return_value = mock_response
        
        method_func = getattr(api_tool, method)
        result = method_func(param)
        
        assert result["success"] is True
        mock_get.assert_called_once()
    
    def test_make_request_url_construction(self, api_tool):
        """Test that _make_request constructs URLs correctly."""
        with patch('src.agent_tools.api_tool_refactored.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {}
            mock_get.return_value = mock_response
            
            api_tool._make_request("/test", {"param1": "value1", "param2": "value2"})
            
            called_url = mock_get.call_args[0][0]
            assert api_tool.base_url in called_url
            assert "/test" in called_url
            assert "param1=value1" in called_url
            assert "param2=value2" in called_url
    
    def test_headers_passed_to_request(self, api_tool):
        """Test that headers are correctly passed to requests."""
        with patch('src.agent_tools.api_tool_refactored.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {}
            mock_get.return_value = mock_response
            
            api_tool.fetch_weather("Test")
            
            call_kwargs = mock_get.call_args[1]
            assert "headers" in call_kwargs
            assert call_kwargs["headers"]["Authorization"] == "Bearer test_api_key"
    
    def test_response_format_consistency(self, api_tool):
        """Test that all methods return consistent response format."""
        with patch('src.agent_tools.api_tool_refactored.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"test": "data"}
            mock_get.return_value = mock_response
            
            for method in [api_tool.fetch_weather, api_tool.fetch_news, api_tool.fetch_stock_price]:
                result = method("test")
                assert "success" in result
                assert "error" in result
                assert "data" in result


class TestAPIToolComparison:
    """Comparison tests between original and refactored implementations."""
    
    @pytest.fixture
    def original_tool(self):
        """Create original API tool."""
        return APITool("https://api.example.com", "test_key")
    
    @pytest.fixture
    def refactored_tool(self):
        """Create refactored API tool."""
        return APIToolRefactored("https://api.example.com", "test_key")
    
    @patch('src.agent_tools.api_tool.requests.get')
    @patch('src.agent_tools.api_tool_refactored.requests.get')
    def test_fetch_weather_output_match(self, mock_refact_get, mock_orig_get, 
                                        original_tool, refactored_tool):
        """Test that original and refactored fetch_weather produce same output."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"temp": 75, "condition": "cloudy"}
        
        mock_orig_get.return_value = mock_response
        mock_refact_get.return_value = mock_response
        
        original_result = original_tool.fetch_weather("Chicago")
        refactored_result = refactored_tool.fetch_weather("Chicago")
        
        assert original_result["success"] == refactored_result["success"]
        assert original_result["data"] == refactored_result["data"]
    
    @patch('src.agent_tools.api_tool.requests.get')
    @patch('src.agent_tools.api_tool_refactored.requests.get')
    def test_fetch_news_output_match(self, mock_refact_get, mock_orig_get,
                                     original_tool, refactored_tool):
        """Test that original and refactored fetch_news produce same output."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"articles": ["news1", "news2"]}
        
        mock_orig_get.return_value = mock_response
        mock_refact_get.return_value = mock_response
        
        original_result = original_tool.fetch_news("tech")
        refactored_result = refactored_tool.fetch_news("tech")
        
        assert original_result["success"] == refactored_result["success"]
        assert original_result["data"] == refactored_result["data"]
    
    @patch('src.agent_tools.api_tool.requests.get')
    @patch('src.agent_tools.api_tool_refactored.requests.get')
    def test_fetch_stock_price_output_match(self, mock_refact_get, mock_orig_get,
                                           original_tool, refactored_tool):
        """Test that original and refactored fetch_stock_price produce same output."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"symbol": "MSFT", "price": 300.50}
        
        mock_orig_get.return_value = mock_response
        mock_refact_get.return_value = mock_response
        
        original_result = original_tool.fetch_stock_price("MSFT")
        refactored_result = refactored_tool.fetch_stock_price("MSFT")
        
        assert original_result["success"] == refactored_result["success"]
        assert original_result["data"] == refactored_result["data"]
    
    @patch('src.agent_tools.api_tool.requests.get')
    @patch('src.agent_tools.api_tool_refactored.requests.get')
    def test_timeout_error_format_match(self, mock_refact_get, mock_orig_get,
                                       original_tool, refactored_tool):
        """Test that timeout errors have same format."""
        mock_orig_get.side_effect = requests.Timeout("Timeout")
        mock_refact_get.side_effect = requests.Timeout("Timeout")
        
        original_result = original_tool.fetch_weather("Test")
        refactored_result = refactored_tool.fetch_weather("Test")
        
        assert original_result["success"] == refactored_result["success"]
        assert original_result["success"] is False
        assert original_result["data"] is None
        assert refactored_result["data"] is None
    
    @patch('src.agent_tools.api_tool.requests.get')
    @patch('src.agent_tools.api_tool_refactored.requests.get')
    def test_http_error_format_match(self, mock_refact_get, mock_orig_get,
                                    original_tool, refactored_tool):
        """Test that HTTP errors have same format."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        
        mock_orig_get.return_value = mock_response
        mock_refact_get.return_value = mock_response
        
        original_result = original_tool.fetch_news("test")
        refactored_result = refactored_tool.fetch_news("test")
        
        assert original_result["success"] == refactored_result["success"]
        assert original_result["success"] is False
        assert "500" in original_result["error"]
        assert "500" in refactored_result["error"]
