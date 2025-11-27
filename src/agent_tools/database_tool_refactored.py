"""
Refactored Database Tool for AI Agent
- Eliminates duplication via a generic query template
- Uses parameterized SQL to avoid injection
- Config-driven table/field mapping
"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Any, Callable, Dict, Iterable, List

from .base_tool import BaseTool


DB_CONFIG: Dict[str, Dict[str, Any]] = {
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


class DatabaseToolRefactored(BaseTool):
    def __init__(
        self,
        connection_string: str,
        config: Dict[str, Dict[str, Any]] | None = None,
        connection_factory: Callable[[str], Any] | None = None,
    ) -> None:
        super().__init__()
        self.connection_string = connection_string
        self.config: Dict[str, Dict[str, Any]] = config or DB_CONFIG
        # Allow injecting a custom connection factory for tests
        self.connection_factory = connection_factory or sqlite3.connect

    @contextmanager
    def _connect(self):
        conn = None
        try:
            conn = self.connection_factory(self.connection_string)
            yield conn
        finally:
            if conn:
                try:
                    conn.close()
                except Exception:
                    # Closing errors are non-critical for these tools
                    pass

    def _build_query(self, query_type: str) -> str:
        conf = self.config.get(query_type)
        if conf is None:
            raise ValueError(f"Unsupported query type: {query_type}")
        fields = ", ".join(conf["fields"])
        table = conf["table"]
        return f"SELECT {fields} FROM {table} WHERE id = ?"

    def _normalize_rows(self, query_type: str, rows: Iterable[Iterable[Any]]) -> List[Dict[str, Any]]:
        fields = self.config[query_type]["fields"]
        return [dict(zip(fields, row)) for row in rows]

    def _execute_query(self, query_type: str, entity_id: Any) -> List[Dict[str, Any]]:
        sql = self._build_query(query_type)
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (entity_id,))
            rows = cursor.fetchall()
        return self._normalize_rows(query_type, rows)

    @BaseTool.error_handler
    def query(self, query_type: str, entity_id: Any):
        data = self._execute_query(query_type, entity_id)
        self.logger.info("Query %s successful, returned %d rows", query_type, len(data))
        return self.format_response(True, data=data)

    def query_users(self, user_id: Any):
        return self.query("users", user_id)

    def query_products(self, product_id: Any):
        return self.query("products", product_id)

    def query_orders(self, order_id: Any):
        return self.query("orders", order_id)
