"""
API Tool for AI Agent - Refactored
Handles external API calls with unified error handling and request logic
"""
import requests
from typing import Dict, Any, Optional
import logging

from base_tool import BaseTool


class APIToolRefactored(BaseTool):
    """Refactored API tool using generic request method and unified error handling"""
    
    # Configuration for different API endpoints
    ENDPOINT_CONFIG = {
        "weather": {
            "path": "/weather",
            "params_key": "city"
        },
        "news": {
            "path": "/news",
            "params_key": "category"
        },
        "stock": {
            "path": "/stock",
            "params_key": "symbol"
        }
    }
    
    DEFAULT_TIMEOUT = 10
    
    def __init__(self, base_url: str, api_key: str):
        """Initialize APIToolRefactored"""
        super().__init__(logger_name=__name__)
        self.base_url = base_url
        self.api_key = api_key
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Centralized method to get request headers - eliminates duplication
        
        Returns:
            Headers dictionary with authorization and content type
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, endpoint_type: str, param_value: str) -> Dict[str, Any]:
        """
        Generic request method - eliminates duplication across fetch methods
        
        Args:
            endpoint_type: Type of endpoint (weather, news, stock)
            param_value: Value for the parameter (city, category, symbol)
            
        Returns:
            Formatted response with API data
        """
        if endpoint_type not in self.ENDPOINT_CONFIG:
            return self.format_response(
                success=False,
                error=f"Unknown endpoint type: {endpoint_type}",
                data=None
            )
        
        try:
            config = self.ENDPOINT_CONFIG[endpoint_type]
            param_key = config["params_key"]
            path = config["path"]
            
            # Build URL and prepare request
            url = f"{self.base_url}{path}?{param_key}={param_value}"
            headers = self._get_headers()
            
            self.logger.info(f"Making request to {endpoint_type} endpoint with {param_key}={param_value}")
            self.logger.debug(f"Request URL: {url}")
            
            # Make unified request
            response = self._make_http_request(url, headers)
            
            if response.status_code != 200:
                error_msg = f"HTTP {response.status_code}"
                self.logger.error(f"API request failed: {error_msg}")
                return self.format_response(
                    success=False,
                    error=error_msg,
                    data=None
                )
            
            # Parse response
            data = response.json()
            self.logger.info(f"{endpoint_type.capitalize()} data fetched successfully")
            return self.format_response(
                success=True,
                data=data,
                error=None
            )
        
        except requests.Timeout:
            error_msg = "Request timeout"
            self.logger.error(error_msg)
            return self.format_response(
                success=False,
                error=error_msg,
                data=None
            )
        except requests.RequestException as e:
            error_msg = f"Request error: {str(e)}"
            self.logger.error(error_msg)
            return self.format_response(
                success=False,
                error=error_msg,
                data=None
            )
        except Exception as e:
            error_msg = f"Error making request: {str(e)}"
            self.logger.error(error_msg)
            return self.format_response(
                success=False,
                error=error_msg,
                data=None
            )
    
    def fetch_weather(self, city: str) -> Dict[str, Any]:
        """Fetch weather data from API"""
        return self._make_request("weather", city)
    
    def fetch_news(self, category: str) -> Dict[str, Any]:
        """Fetch news data from API"""
        return self._make_request("news", category)
    
    def fetch_stock_price(self, symbol: str) -> Dict[str, Any]:
        """Fetch stock price from API"""
        return self._make_request("stock", symbol)
    
    def _make_http_request(self, url: str, headers: Dict[str, str]) -> requests.Response:
        """
        Wrapper for HTTP requests - allows for easy mocking in tests
        
        Args:
            url: URL to request
            headers: Request headers
            
        Returns:
            Response object
        """
        return requests.get(url, headers=headers, timeout=self.DEFAULT_TIMEOUT)
