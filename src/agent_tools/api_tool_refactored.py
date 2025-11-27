"""
Refactored API Tool
- Generic _make_request method
- Centralized header creation and error handling
- Backwards compatible methods
"""
from urllib.parse import urlencode

import requests
from typing import Optional, Dict, Any

from .base_tool import BaseTool


class APIToolRefactored(BaseTool):
    TIMEOUT = 10

    def __init__(self, base_url: str, api_key: str):
        super().__init__()
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _get_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    @BaseTool.error_handler
    def _make_request(self, path: str, params: Optional[Dict[str, Any]] = None) -> dict:
        url = f"{self.base_url}/{path.lstrip('/')}"
        self.logger.info(f"Making request to: {url} with params={params}")
        headers = self._get_headers()
        try:
            response = requests.get(url, headers=headers, params=params, timeout=self.TIMEOUT)
            if response.status_code != 200:
                self.logger.error(f"API request failed with status: {response.status_code}")
                return self.format_response(False, error=f"HTTP {response.status_code}", data=None)

            data = response.json()
            return self.format_response(True, error=None, data=data)
        except requests.Timeout:
            self.logger.error("Request timeout")
            return self.format_response(False, error="Request timeout", data=None)

    def fetch_weather(self, city: str) -> dict:
        return self._make_request("weather", params={"city": city})

    def fetch_news(self, category: str) -> dict:
        return self._make_request("news", params={"category": category})

    def fetch_stock_price(self, symbol: str) -> dict:
        return self._make_request("stock", params={"symbol": symbol})


__all__ = ["APIToolRefactored"]
