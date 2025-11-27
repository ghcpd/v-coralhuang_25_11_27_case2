import pytest
from unittest.mock import patch

from src.agent_tools.database_tool_refactored import DatabaseToolRefactored
from src.agent_tools.database_tool import DatabaseTool as OrigDatabaseTool


@pytest.fixture
def db_tool():
    return DatabaseToolRefactored("sqlite://test")


def test_query_users_success(db_tool):
    fake_rows = [[1, "John", "john@example.com", "2024-01-01"]]
    with patch.object(db_tool, "_execute_query", return_value=fake_rows) as mock_exec:
        result = db_tool.query_users(1)
        assert result["success"] is True
        assert isinstance(result["data"], list)
        assert result["data"][0]["name"] == "John"
        mock_exec.assert_called_once()


@pytest.mark.parametrize("query_type,method_name,entity_id", [
    ("users", "query_users", 1),
    ("products", "query_products", 2),
    ("orders", "query_orders", 3),
])
def test_execute_query_all_types(db_tool, query_type, method_name, entity_id):
    fake_rows = [[entity_id, "X", 3.14, "2024-01-01"]]
    with patch.object(db_tool, "_execute_query", return_value=fake_rows):
        method = getattr(db_tool, method_name)
        result = method(entity_id)
        assert result["success"] is True
        assert isinstance(result["data"], list)


def test_refactored_matches_original(monkeypatch):
    # The original returns a single 'Test' row; patch both to return that row
    orig = OrigDatabaseTool("sqlite://test")
    ref = DatabaseToolRefactored("sqlite://test")
    fake_rows = [[1, "Test", "test@example.com", "2024-01-01"]]
    class Conn:
        def close(self):
            pass

    with patch.object(orig, "_create_connection", return_value=Conn()), patch.object(orig, "_execute_query", return_value=fake_rows), patch.object(ref, "_execute_query", return_value=fake_rows):
        a = orig.query_users(1)
        b = ref.query_users(1)
        assert a["success"] == b["success"]
        assert a["data"] is not None and b["data"] is not None
        # Compare core fields
        assert a["data"][0]["id"] == b["data"][0]["id"]
