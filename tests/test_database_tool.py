import sqlite3
from typing import Any

import pytest

from src.agent_tools.database_tool import DatabaseTool
from src.agent_tools.database_tool_refactored import DatabaseToolRefactored, DB_CONFIG


@pytest.fixture
def db_path(tmp_path):
    return tmp_path / "test.db"


@pytest.fixture
def setup_db(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # Create tables
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, created_at TEXT)")
    cur.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER)")
    cur.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, total REAL, status TEXT)")
    # Seed data
    cur.execute("INSERT INTO users VALUES (1, 'John', 'john@example.com', '2024-01-01')")
    cur.execute("INSERT INTO products VALUES (1, 'Widget', 9.99, 100)")
    cur.execute("INSERT INTO orders VALUES (1, 1, 19.99, 'shipped')")
    conn.commit()
    conn.close()


@pytest.fixture
def db_tool_refactored(db_path, setup_db):
    return DatabaseToolRefactored(connection_string=str(db_path))


@pytest.fixture
def db_tool_original(db_path, setup_db, monkeypatch):
    tool = DatabaseTool(connection_string=str(db_path))

    def _create_connection(self):
        return sqlite3.connect(self.connection_string)

    def _execute_query(self, connection, query: str):
        cur = connection.cursor()
        cur.execute(query)
        return cur.fetchall()

    monkeypatch.setattr(tool, "_create_connection", _create_connection.__get__(tool, DatabaseTool))
    monkeypatch.setattr(tool, "_execute_query", _execute_query.__get__(tool, DatabaseTool))
    return tool


def test_query_users_success(db_tool_refactored):
    result = db_tool_refactored.query_users(1)
    assert result["success"] is True
    assert result["data"][0]["email"] == "john@example.com"


def test_query_products_success(db_tool_refactored):
    result = db_tool_refactored.query_products(1)
    assert result["success"] is True
    assert result["data"][0]["price"] == 9.99


def test_query_orders_success(db_tool_refactored):
    result = db_tool_refactored.query_orders(1)
    assert result["success"] is True
    assert result["data"][0]["status"] == "shipped"


@pytest.mark.parametrize("query_type", ["users", "products", "orders"])
def test_execute_query_all_types(db_tool_refactored, query_type):
    data = db_tool_refactored._execute_query(query_type, 1)
    fields = DB_CONFIG[query_type]["fields"]
    assert all(field in data[0] for field in fields)


def test_query_unknown_type_returns_error(db_tool_refactored):
    res = db_tool_refactored.query("unknown", 1)
    assert res["success"] is False
    assert "Unsupported" in res["error"]


def test_original_vs_refactored_output_match(db_tool_original, db_tool_refactored):
    # Compare data payloads for same ID across original and refactored implementations
    orig = db_tool_original.query_users(1)
    ref = db_tool_refactored.query_users(1)
    assert orig["success"] == ref["success"]
    # Map original list of dicts to comparable keys
    assert orig["data"][0]["email"] == ref["data"][0]["email"]


def test_sql_injection_protection(db_tool_refactored):
    # Ensure parameterized query uses placeholders
    sql = db_tool_refactored._build_query("users")
    assert "WHERE id = ?" in sql
    # A malicious-looking input should be treated as a value and return empty data
    malicious_id = "1; DROP TABLE users; --"
    res = db_tool_refactored.query_users(malicious_id)
    assert res["success"] is True
    assert res["data"] == []
