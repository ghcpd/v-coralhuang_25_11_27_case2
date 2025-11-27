"""
Refactored Database Tool
Uses parameterized queries, context manager for connections, and shared BaseTool utilities
"""
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
import logging

from .base_tool import BaseTool


class DatabaseToolRefactored(BaseTool):
    CONFIG = {
        "users": {"table": "users", "fields": ["id", "name", "email", "created_at"]},
        "products": {"table": "products", "fields": ["id", "name", "price", "stock"]},
        "orders": {"table": "orders", "fields": ["id", "user_id", "total", "status"]},
    }

    def __init__(self, connection_string: str):
        super().__init__()
        self.connection_string = connection_string

    @contextmanager
    def _connection(self):
        self.logger.info(f"Connecting to database: {self.connection_string}")
        conn = self._create_connection()
        try:
            if conn is None:
                self.logger.error("Failed to connect to database")
                raise ConnectionError("Connection failed")
            yield conn
        finally:
            if conn:
                # simulate closing
                try:
                    conn.close()
                except Exception:
                    pass

    def _create_connection(self):
        # Simulated connection that supports close()
        class _Conn:
            def close(self):
                return True

        return _Conn()

    def _execute_query(self, connection, query: str, params: Optional[List[Any]] = None) -> Optional[List[List[Any]]]:
        """Execute a simulated database query. For a real DB, replace with DB driver logic."""
        self.logger.info(f"Executing query: {query} params: {params}")
        # Simulate all queries returning a single example row
        return [[1, "Test", "test@example.com", "2024-01-01"]]

    def _process_rows(self, rows: List[List[Any]], fields: List[str]) -> List[Dict[str, Any]]:
        processed = []
        for r in rows:
            processed.append({fields[i]: r[i] for i in range(min(len(fields), len(r)))})
        return processed

    @BaseTool.handle_errors
    def _execute(self, query_type: str, entity_id: int):
        if query_type not in self.CONFIG:
            raise ValueError("Unknown query type")
        cfg = self.CONFIG[query_type]
        fields = cfg["fields"]
        table = cfg["table"]
        sql = f"SELECT {', '.join(fields)} FROM {table} WHERE id = ?"
        with self._connection() as conn:
            result = self._execute_query(conn, sql, [entity_id])
            if result is None:
                return self.format_response(False, data=None, error="Query failed")
            processed = self._process_rows(result, fields)
            self.logger.info(f"Query successful, returned {len(processed)} rows")
            return self.format_response(True, data=processed)

    # Convenience methods
    def query_users(self, user_id: int):
        return self._execute("users", user_id)

    def query_products(self, product_id: int):
        return self._execute("products", product_id)

    def query_orders(self, order_id: int):
        return self._execute("orders", order_id)


__all__ = ["DatabaseToolRefactored"]
