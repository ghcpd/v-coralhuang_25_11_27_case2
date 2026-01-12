"""
Refactored API Tool for AI Agent
Eliminates code duplication using generic request method and unified error handling.
"""
import requests
from typing import Dict, Any, Optional
from .base_tool import BaseTool


class APIToolRefactored(BaseTool):
    """Refactored API tool with eliminated duplication and improved error handling."""
    
    def __init__(self, base_url: str, api_key: str):
        """
        Initialize API tool with base URL and API key.
        
        Args:
            base_url: Base URL for API requests
            api_key: API authentication key
        """
        super().__init__()
        self.base_url = base_url
        self.api_key = api_key
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Get standardized headers for API requests.
        
        Returns:
            Dictionary of HTTP headers
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, endpoint: str, params: Dict[str, str]) -> Dict[str, Any]:
        """
        Generic method to make API requests with unified error handling.
        
        Args:
            endpoint: API endpoint path (e.g., "/weather")
            params: Query parameters as dictionary
        
        Returns:
            Standardized response dictionary
        """
        # Construct URL with parameters
        param_string = "&".join([f"{k}={v}" for k, v in params.items()])
        url = f"{self.base_url}{endpoint}?{param_string}"
        
        self._log_operation(f"Making request to: {url}")
        
        try:
            # Make HTTP request with timeout
            response = requests.get(
                url,
                headers=self._get_headers(),
                timeout=10
            )
            
            # Check response status
            if response.status_code != 200:
                error_msg = f"HTTP {response.status_code}"
                self.logger.error(f"API request failed with status: {response.status_code}")
                return self.format_response(success=False, error=error_msg)
            
            # Parse and return successful response
            data = response.json()
            self._log_operation(f"Request successful for {endpoint}")
            return self.format_response(success=True, data=data)
            
        except requests.Timeout:
            self.logger.error("Request timeout")
            return self.format_response(success=False, error="Request timeout")
        except requests.RequestException as e:
            self.logger.error(f"Request error: {str(e)}")
            return self.format_response(success=False, error=str(e))
        except ValueError as e:
            self.logger.error(f"JSON parsing error: {str(e)}")
            return self.format_response(success=False, error=f"Invalid JSON response: {str(e)}")
    
    @BaseTool.handle_errors("API request")
    def fetch_weather(self, city: str) -> Dict[str, Any]:
        """
        Fetch weather data from API.
        
        Args:
            city: Name of the city
        
        Returns:
            Standardized response with weather data
        """
        self._log_operation(f"Fetching weather data for city: {city}")
        return self._make_request("/weather", {"city": city})
    
    @BaseTool.handle_errors("API request")
    def fetch_news(self, category: str) -> Dict[str, Any]:
        """
        Fetch news data from API.
        
        Args:
            category: News category
        
        Returns:
            Standardized response with news data
        """
        self._log_operation(f"Fetching news data for category: {category}")
        return self._make_request("/news", {"category": category})
    
    @BaseTool.handle_errors("API request")
    def fetch_stock_price(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch stock price from API.
        
        Args:
            symbol: Stock symbol
        
        Returns:
            Standardized response with stock price data
        """
        self._log_operation(f"Fetching stock price for symbol: {symbol}")
        return self._make_request("/stock", {"symbol": symbol})
