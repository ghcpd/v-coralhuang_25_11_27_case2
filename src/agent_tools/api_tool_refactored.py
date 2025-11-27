"""
Refactored API Tool with a generic request method and unified error handling
"""
from typing import Any, Dict, Optional, Callable
import requests
from .base_tool import BaseTool, handle_errors
import logging


class APIToolRefactored(BaseTool):
    def __init__(self, base_url: str, api_key: str, request_fn: Optional[Callable] = None):
        super().__init__()
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.logger = logging.getLogger(self.__class__.__name__)
        # request_fn injection to make testing trivial
        self._request_fn = request_fn or requests.get

    def _get_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def _make_request(self, path: str, params: Optional[Dict[str, Any]] = None):
        url = f"{self.base_url}/{path.lstrip('/') }"
        self.logger.info("Making request to %s with params=%s", url, params)
        try:
            response = self._request_fn(url, headers=self._get_headers(), params=params, timeout=10)
        except Exception as exc:
            self.logger.exception("Request error")
            return self.format_response(False, str(exc), None)

        if getattr(response, "status_code", None) != 200:
            self.logger.error("API request failed with status: %s", getattr(response, "status_code", None))
            return self.format_response(False, f"HTTP {getattr(response, 'status_code', 'N/A')}", None)

        # In many cases API returns JSON; preserve that structure
        try:
            data = response.json()
        except Exception:
            data = response.text if hasattr(response, "text") else None

        return self.format_response(True, None, data)

    # Backwards compatible methods
    @handle_errors
    def fetch_weather(self, city: str):
        return self._make_request("weather", params={"city": city})

    @handle_errors
    def fetch_news(self, category: str):
        return self._make_request("news", params={"category": category})

    @handle_errors
    def fetch_stock_price(self, symbol: str):
        return self._make_request("stock", params={"symbol": symbol})
