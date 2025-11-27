import pytest
from unittest.mock import patch

from src.agent_tools.database_tool import DatabaseTool as LegacyDB
from src.agent_tools.database_tool_refactored import DatabaseToolRefactored


@pytest.fixture
def sample_row():
    return [1, "John", "john@example.com", "2024-01-01"]


@pytest.fixture
def legacy_db():
    return LegacyDB("sqlite://memory")


@pytest.fixture
def refactored_db(sample_row):
    # Inject an execute function that returns the sample row
    def exec_fn(conn, query, params=None):
        return [sample_row]

    return DatabaseToolRefactored("sqlite://memory", execute_fn=exec_fn)


def test_query_users_success_matches_legacy(legacy_db, refactored_db, sample_row):
    # Ensure legacy connection has a close method to avoid AttributeError
    class Conn:
        def close(self):
            pass

    with patch.object(legacy_db, "_create_connection", return_value=Conn()), patch.object(legacy_db, "_execute_query", return_value=[sample_row]):
        legacy_res = legacy_db.query_users(1)
    refactored_res = refactored_db.query_users(1)
    assert legacy_res["success"] == refactored_res["success"]
    assert legacy_res["data"] == refactored_res["data"]


@pytest.mark.parametrize("query_type,method", [
    ("users", "query_users"),
    ("products", "query_products"),
    ("orders", "query_orders"),
])
def test_execute_query_all_types(refactored_db, query_type, method):
    # Ensure generic method handles all configured types
    fn = getattr(refactored_db, method)
    res = fn(1)
    assert res["success"] is True
    assert isinstance(res["data"], list)
