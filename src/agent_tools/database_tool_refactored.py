"""
Refactored Database Tool
- Generic _execute_query method
- Config-driven mapping for entities
- Parameterized queries
- Context manager for connection
"""
from contextlib import contextmanager
from typing import Any, Dict, Optional, List

from .base_tool import BaseTool


class DatabaseToolRefactored(BaseTool):
    DEFAULT_CONFIG = {
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

    def __init__(self, connection_string: str, config: Optional[Dict] = None):
        super().__init__()
        self.connection_string = connection_string
        self.config = config or self.DEFAULT_CONFIG

    @contextmanager
    def _connect(self):
        """Context manager for database connection (simulated)."""
        self.logger.info(f"Connecting to database: {self.connection_string}")
        conn = self._create_connection()
        try:
            if conn is None:
                self.logger.error("Failed to connect to database")
                yield None
            else:
                yield conn
        finally:
            if conn:
                try:
                    conn.close()
                except Exception:
                    # Some simulated connections may not support close
                    pass

    def _create_connection(self):
        """Simulated DB connection. In real-world, return actual DB connection."""
        return {"status": "connected"}

    def _execute(self, connection: Any, query: str, params: Optional[tuple] = None) -> Optional[List]:
        """Execute the query against the connection. Simulated here for tests to patch."""
        # The real implementation would run cursor.execute(query, params)
        # To keep compatibility with the legacy tool, return a simple row structure
        return [[1, "Test", "test@example.com", "2024-01-01"]]

    def _format_rows(self, entity: str, rows: List) -> List[Dict]:
        fields = self.config[entity]["fields"]
        processed = []
        for row in rows:
            processed.append({fields[i]: row[i] for i in range(len(fields))})
        return processed

    def _build_query(self, entity: str) -> str:
        table = self.config[entity]["table"]
        fields = ", ".join(self.config[entity]["fields"])
        # Use parameterized placeholder for safety; actual DB API will handle params
        return f"SELECT {fields} FROM {table} WHERE id = ?"

    @BaseTool.error_handler
    def _execute_query(self, entity: str, entity_id: int) -> dict:
        """Generic query method for users/products/orders"""
        if entity not in self.config:
            return self.format_response(False, error="Unknown entity", data=None)

        query = self._build_query(entity)
        self.logger.info(f"Executing query: {query} with id={entity_id}")

        with self._connect() as conn:
            if conn is None:
                return self.format_response(False, error="Connection failed", data=None)

            result = self._execute(conn, query, params=(entity_id,))

            if result is None:
                return self.format_response(False, error="Query failed", data=None)

            processed = self._format_rows(entity, result)
            return self.format_response(True, error=None, data=processed)

    # Backwards compatible API
    def query_users(self, user_id: int) -> dict:
        return self._execute_query("users", user_id)

    def query_products(self, product_id: int) -> dict:
        return self._execute_query("products", product_id)

    def query_orders(self, order_id: int) -> dict:
        return self._execute_query("orders", order_id)


__all__ = ["DatabaseToolRefactored"]
