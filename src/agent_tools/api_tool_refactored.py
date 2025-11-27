"""
Refactored API Tool for AI Agent
- Centralizes request logic and headers
- Provides unified error handling
- Config-driven endpoints and parameter keys
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import requests

from .base_tool import BaseTool


API_CONFIG: Dict[str, Dict[str, str]] = {
    "weather": {"endpoint": "/weather", "param_key": "city"},
    "news": {"endpoint": "/news", "param_key": "category"},
    "stock_price": {"endpoint": "/stock", "param_key": "symbol"},
}


class APIToolRefactored(BaseTool):
    def __init__(
        self,
        base_url: str,
        api_key: str,
        config: Dict[str, Dict[str, str]] | None = None,
        session: Any = None,
        timeout: int = 10,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        super().__init__(logger=logger)
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.config = config or API_CONFIG
        # session can be requests or requests.Session; default to requests module
        self.session = session or requests

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _make_request(self, config_key: str, value: Any) -> Any:
        conf = self.config.get(config_key)
        if conf is None:
            raise ValueError(f"Unsupported request type: {config_key}")
        endpoint = conf["endpoint"]
        param_key = conf["param_key"]
        url = f"{self.base_url}{endpoint}"
        params = {param_key: value}
        response = self.session.get(url, headers=self._get_headers(), params=params, timeout=self.timeout)
        if response.status_code != 200:
            # Let decorator wrap into a formatted response
            raise requests.HTTPError(f"HTTP {response.status_code}")
        try:
            return response.json()
        except ValueError as exc:
            raise ValueError("Invalid JSON response") from exc

    @BaseTool.error_handler
    def fetch_weather(self, city: str):
        data = self._make_request("weather", city)
        self.logger.info("Weather data fetched")
        return self.format_response(True, data=data)

    @BaseTool.error_handler
    def fetch_news(self, category: str):
        data = self._make_request("news", category)
        self.logger.info("News data fetched")
        return self.format_response(True, data=data)

    @BaseTool.error_handler
    def fetch_stock_price(self, symbol: str):
        data = self._make_request("stock_price", symbol)
        self.logger.info("Stock price fetched")
        return self.format_response(True, data=data)
