"""
Refactored DatabaseTool with generic query execution
Uses a config-driven approach to avoid duplication across types
"""
from typing import Any, Dict, List, Optional
from .base_tool import BaseTool, handle_errors
import logging


class DatabaseToolRefactored(BaseTool):
    """Generic database tool

    This implementation centralizes connection handling, response formatting,
    and query execution so specific query methods can be one-liners that only
    declare intent/parameters.
    """

    CONFIG = {
        "users": {
            "table": "users",
            "fields": ["id", "name", "email", "created_at"],
        },
        "products": {
            "table": "products",
            "fields": ["id", "name", "price", "stock"],
        },
        "orders": {
            "table": "orders",
            "fields": ["id", "user_id", "total", "status"],
        },
    }

    def __init__(self, connection_string: str, execute_fn: Optional[callable] = None):
        super().__init__()
        self.connection_string = connection_string
        self.logger = logging.getLogger(self.__class__.__name__)
        # execute_fn can be injected for tests; when None, use default simulation
        self._execute_fn = execute_fn or self._simulate_execute

    def _create_connection(self) -> Dict[str, str]:
        """Simulated DB connection method (kept for parity with legacy code)."""
        self.logger.debug("Creating DB connection")
        return {"status": "connected"}

    def _simulate_execute(self, connection: Dict, query: str, params: Optional[List[Any]] = None):
        """Default execute function for simulation. Returns sample data."""
        self.logger.debug("Simulated execute called: query=%s params=%s", query, params)
        # Always return a single row for parity with existing helpers
        return [[1, "Test", "test@example.com", "2024-01-01"]]

    def _execute_query(self, query_type: str, entity_id: int):
        """Generic method to execute paramterized queries for known types."""
        cfg = self.CONFIG.get(query_type)
        if not cfg:
            raise ValueError(f"Unknown query_type: {query_type}")

        table = cfg["table"]
        placeholder = "?"
        query = f"SELECT * FROM {table} WHERE id = {placeholder}"

        connection = None
        try:
            self.logger.info(f"Connecting to database: {self.connection_string}")
            connection = self._create_connection()
            if connection is None:
                self.logger.error("Failed to connect to database")
                return self.format_response(False, "Connection failed", None)

            self.logger.info("Executing query: %s -- params=%s", query, [entity_id])
            result = self._execute_fn(connection, query, [entity_id])
            if result is None:
                self.logger.error("Query execution failed")
                return self.format_response(False, "Query failed", None)

            # Build result objects using configured fields
            processed = []
            for row in result:
                obj = {k: v for k, v in zip(cfg["fields"], row)}
                processed.append(obj)

            return self.format_response(True, None, processed)
        except Exception as exc:
            self.logger.exception("Error while executing query")
            return self.format_response(False, str(exc), None)
        finally:
            if connection:
                # In a real DB we'd close; here it's a dict for simulation
                self.logger.debug("Closing connection")

    # Backwards-compatible convenience methods
    @handle_errors
    def query_users(self, user_id: int):
        return self._execute_query("users", user_id)

    @handle_errors
    def query_products(self, product_id: int):
        return self._execute_query("products", product_id)

    @handle_errors
    def query_orders(self, order_id: int):
        return self._execute_query("orders", order_id)
