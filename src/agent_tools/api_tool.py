"""
API Tool for AI Agent
Handles external API calls
"""
import requests
import logging

class APITool:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)
    
    def fetch_weather(self, city):
        """Fetch weather data from API"""
        try:
            self.logger.info(f"Fetching weather data for city: {city}")
            
            # Prepare headers
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Make request
            url = f"{self.base_url}/weather?city={city}"
            self.logger.info(f"Making request to: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                self.logger.error(f"API request failed with status: {response.status_code}")
                return {"success": False, "error": f"HTTP {response.status_code}", "data": None}
            
            # Parse response
            data = response.json()
            self.logger.info("Weather data fetched successfully")
            return {"success": True, "error": None, "data": data}
            
        except requests.Timeout:
            self.logger.error("Request timeout")
            return {"success": False, "error": "Request timeout", "data": None}
        except Exception as e:
            self.logger.error(f"Error fetching weather: {str(e)}")
            return {"success": False, "error": str(e), "data": None}
    
    def fetch_news(self, category):
        """Fetch news data from API"""
        try:
            self.logger.info(f"Fetching news data for category: {category}")
            
            # Prepare headers
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Make request
            url = f"{self.base_url}/news?category={category}"
            self.logger.info(f"Making request to: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                self.logger.error(f"API request failed with status: {response.status_code}")
                return {"success": False, "error": f"HTTP {response.status_code}", "data": None}
            
            # Parse response
            data = response.json()
            self.logger.info("News data fetched successfully")
            return {"success": True, "error": None, "data": data}
            
        except requests.Timeout:
            self.logger.error("Request timeout")
            return {"success": False, "error": "Request timeout", "data": None}
        except Exception as e:
            self.logger.error(f"Error fetching news: {str(e)}")
            return {"success": False, "error": str(e), "data": None}
    
    def fetch_stock_price(self, symbol):
        """Fetch stock price from API"""
        try:
            self.logger.info(f"Fetching stock price for symbol: {symbol}")
            
            # Prepare headers
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Make request
            url = f"{self.base_url}/stock?symbol={symbol}"
            self.logger.info(f"Making request to: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                self.logger.error(f"API request failed with status: {response.status_code}")
                return {"success": False, "error": f"HTTP {response.status_code}", "data": None}
            
            # Parse response
            data = response.json()
            self.logger.info("Stock price fetched successfully")
            return {"success": True, "error": None, "data": data}
            
        except requests.Timeout:
            self.logger.error("Request timeout")
            return {"success": False, "error": "Request timeout", "data": None}
        except Exception as e:
            self.logger.error(f"Error fetching stock price: {str(e)}")
            return {"success": False, "error": str(e), "data": None}
