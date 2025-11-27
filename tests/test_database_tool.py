import pytest
from unittest.mock import patch

from src.agent_tools.database_tool import DatabaseTool as OriginalDB
from src.agent_tools.database_tool_refactored import DatabaseToolRefactored


@pytest.fixture
def sample_rows():
    return [[1, "John", "john@example.com", "2024-01-01"]]


@pytest.fixture
def orig_db():
    return OriginalDB("sqlite:///:memory:")


@pytest.fixture
def ref_db():
    return DatabaseToolRefactored("sqlite:///:memory:")


def test_query_users_success(ref_db, sample_rows):
    # Patch the low-level _execute to return a predictable result
    with patch.object(ref_db, "_execute", return_value=sample_rows) as mock_exec:
        res = ref_db.query_users(1)
        assert res["success"] is True
        assert isinstance(res["data"], list)
        mock_exec.assert_called_once()


@pytest.mark.parametrize("entity", ["users", "products", "orders"])
def test_execute_query_all_types(ref_db, entity, sample_rows):
    with patch.object(ref_db, "_execute", return_value=sample_rows) as mock_exec:
        res = ref_db._execute_query(entity, 1)
        assert res["success"] is True
        assert isinstance(res["data"], list)
        assert len(res["data"]) == 1
        # Ensure the values map to keys provided by config
        keys = list(res["data"][0].keys())
        assert len(keys) == len(ref_db.config[entity]["fields"])


def test_parameterized_query_prevents_sql_injection(ref_db, sample_rows):
    # Ensure that the query uses a placeholder and params tuple rather than string formatting
    with patch.object(ref_db, "_execute", return_value=sample_rows) as mock_exec:
        malicious_id = "1; DROP TABLE users;"
        res = ref_db.query_users(malicious_id)
        assert res["success"] is True
        # Ensure the query string contains placeholder '?'
        called_query = mock_exec.call_args[0][1]
        assert "?" in called_query
        # And that params contains the malicious string, not inserted into the query
        called_params = mock_exec.call_args[1].get("params") or mock_exec.call_args[0][2]
        assert called_params[0] == malicious_id


def test_original_and_refactored_output_match(orig_db, ref_db, sample_rows):
    # Patch original's _execute_query (internal) method to be deterministic
    class DummyConn:
        def close(self):
            return

    with patch.object(orig_db, "_execute_query", return_value=sample_rows):
        # Ensure closing won't fail
        with patch.object(orig_db, "_create_connection", return_value=DummyConn()):
            orig_res = orig_db.query_users(1)

    with patch.object(ref_db, "_execute", return_value=sample_rows):
        ref_res = ref_db.query_users(1)

    # Compare the 'data' parts; both return list of dicts, but orig returns list of dicts too
    assert orig_res["success"] == ref_res["success"]
    assert isinstance(orig_res["data"], list) and isinstance(ref_res["data"], list)
    # Convert to comparable structure (list of tuples) to compare
    orig_tuple = tuple(tuple(sorted(d.items())) for d in orig_res["data"]) if orig_res["data"] else ()
    ref_tuple = tuple(tuple(sorted(d.items())) for d in ref_res["data"]) if ref_res["data"] else ()
    assert orig_tuple == ref_tuple


@pytest.mark.parametrize("method,entity", [("query_users", "users"), ("query_products", "products"), ("query_orders", "orders")])
def test_all_methods_match(orig_db, ref_db, sample_rows, method, entity):
    class DummyConn:
        def close(self):
            return

    # Patch original's low-level call for deterministic output
    with patch.object(orig_db, "_execute_query", return_value=sample_rows):
        with patch.object(orig_db, "_create_connection", return_value=DummyConn()):
            orig_res = getattr(orig_db, method)(1)

    # For refactored, patch the _execute to return same rows
    with patch.object(ref_db, "_execute", return_value=sample_rows):
        ref_res = getattr(ref_db, method)(1)

    assert orig_res["success"] == ref_res["success"]
    orig_tuple = tuple(tuple(sorted(d.items())) for d in orig_res["data"]) if orig_res["data"] else ()
    ref_tuple = tuple(tuple(sorted(d.items())) for d in ref_res["data"]) if ref_res["data"] else ()
    assert orig_tuple == ref_tuple
