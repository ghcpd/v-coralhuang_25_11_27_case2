"""
Refactored API Tool
Uses centralized headers, a generic request method, and BaseTool error handling
"""
from typing import Optional, Dict, Any
import requests

from .base_tool import BaseTool


class APIToolRefactored(BaseTool):
    def __init__(self, base_url: str, api_key: str):
        super().__init__()
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    @BaseTool.handle_errors
    def _make_request(self, endpoint: str, params: Optional[Dict[str, str]] = None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self.logger.info(f"Making request to: {url} params: {params}")
        try:
            resp = requests.get(url, headers=self._get_headers(), params=params, timeout=10)
        except requests.Timeout:
            return self.format_response(False, error="Request timeout")
        if resp.status_code != 200:
            self.logger.error(f"API request failed with status: {resp.status_code}")
            return self.format_response(False, error=f"HTTP {resp.status_code}")
        return self.format_response(True, data=resp.json())

    def fetch_weather(self, city: str):
        return self._make_request("weather", {"city": city})

    def fetch_news(self, category: str):
        return self._make_request("news", {"category": category})

    def fetch_stock_price(self, symbol: str):
        return self._make_request("stock", {"symbol": symbol})


__all__ = ["APIToolRefactored"]
