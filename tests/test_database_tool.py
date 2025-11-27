"""
Unit tests for DatabaseToolRefactored class.
Tests database operations, parameterized queries, and comparison with original.
"""
import pytest
from unittest.mock import patch, MagicMock
from src.agent_tools.database_tool import DatabaseTool
from src.agent_tools.database_tool_refactored import DatabaseToolRefactored


class TestDatabaseToolRefactored:
    """Test suite for refactored database tool."""
    
    @pytest.fixture
    def db_tool(self):
        """Create a DatabaseToolRefactored instance for testing."""
        return DatabaseToolRefactored("test_connection_string")
    
    @pytest.fixture
    def original_db_tool(self):
        """Create original DatabaseTool instance for comparison tests."""
        return DatabaseTool("test_connection_string")
    
    def test_initialization(self, db_tool):
        """Test database tool initialization."""
        assert db_tool.connection_string == "test_connection_string"
        assert hasattr(db_tool, "logger")
    
    def test_query_config_exists(self, db_tool):
        """Test that query configuration is properly defined."""
        assert "users" in db_tool.QUERY_CONFIG
        assert "products" in db_tool.QUERY_CONFIG
        assert "orders" in db_tool.QUERY_CONFIG
        
        # Verify users config
        assert db_tool.QUERY_CONFIG["users"]["table"] == "users"
        assert "id" in db_tool.QUERY_CONFIG["users"]["fields"]
        assert "name" in db_tool.QUERY_CONFIG["users"]["fields"]
    
    def test_query_users_success(self, db_tool):
        """Test successful user query."""
        with patch.object(db_tool, '_execute_raw_query') as mock_execute:
            mock_execute.return_value = [[1, "John", "john@example.com", "2024-01-01"]]
            
            result = db_tool.query_users(1)
            
            assert result["success"] is True
            assert result["error"] is None
            assert len(result["data"]) == 1
            assert result["data"][0]["id"] == 1
            assert result["data"][0]["name"] == "John"
            assert result["data"][0]["email"] == "john@example.com"
    
    def test_query_products_success(self, db_tool):
        """Test successful product query."""
        with patch.object(db_tool, '_execute_raw_query') as mock_execute:
            mock_execute.return_value = [[1, "Widget", 19.99, 100]]
            
            result = db_tool.query_products(1)
            
            assert result["success"] is True
            assert result["data"][0]["name"] == "Widget"
            assert result["data"][0]["price"] == 19.99
            assert result["data"][0]["stock"] == 100
    
    def test_query_orders_success(self, db_tool):
        """Test successful order query."""
        with patch.object(db_tool, '_execute_raw_query') as mock_execute:
            mock_execute.return_value = [[1, 123, 99.99, "completed"]]
            
            result = db_tool.query_orders(1)
            
            assert result["success"] is True
            assert result["data"][0]["user_id"] == 123
            assert result["data"][0]["total"] == 99.99
            assert result["data"][0]["status"] == "completed"
    
    def test_query_connection_error(self, db_tool):
        """Test handling of connection errors."""
        with patch.object(db_tool, '_create_connection') as mock_connect:
            mock_connect.return_value = None
            
            result = db_tool.query_users(1)
            
            assert result["success"] is False
            assert "connection" in result["error"].lower()
    
    def test_query_execution_error(self, db_tool):
        """Test handling of query execution errors."""
        with patch.object(db_tool, '_execute_raw_query') as mock_execute:
            mock_execute.return_value = None
            
            result = db_tool.query_users(1)
            
            assert result["success"] is False
            assert "failed" in result["error"].lower()
    
    @pytest.mark.parametrize("query_type,entity_id", [
        ("users", 1),
        ("products", 2),
        ("orders", 3),
    ])
    def test_execute_query_all_types(self, db_tool, query_type, entity_id):
        """Test generic _execute_query method for all entity types."""
        with patch.object(db_tool, '_execute_raw_query') as mock_execute:
            mock_execute.return_value = [[1, "test", "test", "test"]]
            
            result = db_tool._execute_query(query_type, entity_id)
            
            assert result["success"] is True
            assert len(result["data"]) == 1
    
    def test_execute_query_invalid_type(self, db_tool):
        """Test _execute_query with invalid query type."""
        result = db_tool._execute_query("invalid_type", 1)
        
        assert result["success"] is False
        assert "Invalid query type" in result["error"]
    
    def test_process_results(self, db_tool):
        """Test result processing with field mapping."""
        raw_results = [
            [1, "John", "john@example.com", "2024-01-01"],
            [2, "Jane", "jane@example.com", "2024-01-02"]
        ]
        fields = ["id", "name", "email", "created_at"]
        
        processed = db_tool._process_results(raw_results, fields)
        
        assert len(processed) == 2
        assert processed[0]["id"] == 1
        assert processed[0]["name"] == "John"
        assert processed[1]["id"] == 2
        assert processed[1]["name"] == "Jane"
    
    def test_context_manager_connection(self, db_tool):
        """Test context manager properly manages connections."""
        with patch.object(db_tool, '_create_connection') as mock_connect:
            mock_connection = MagicMock()
            mock_connect.return_value = mock_connection
            
            with db_tool._get_connection() as conn:
                assert conn is not None
            
            mock_connection.close.assert_called_once()
    
    def test_response_format_consistency(self, db_tool):
        """Test that all methods return consistent response format."""
        with patch.object(db_tool, '_execute_raw_query') as mock_execute:
            mock_execute.return_value = [[1, "test", "test", "test"]]
            
            for method in [db_tool.query_users, db_tool.query_products, db_tool.query_orders]:
                result = method(1)
                assert "success" in result
                assert "error" in result
                assert "data" in result


class TestDatabaseToolComparison:
    """Comparison tests between original and refactored implementations."""
    
    @pytest.fixture
    def original_tool(self):
        """Create original database tool."""
        return DatabaseTool("test_connection")
    
    @pytest.fixture
    def refactored_tool(self):
        """Create refactored database tool."""
        return DatabaseToolRefactored("test_connection")
    
    def test_query_users_output_match(self, original_tool, refactored_tool):
        """Test that original and refactored query_users produce same output."""
        with patch.object(original_tool, '_execute_query') as mock_orig, \
             patch.object(refactored_tool, '_execute_raw_query') as mock_refact:
            
            test_data = [[1, "John", "john@example.com", "2024-01-01"]]
            mock_orig.return_value = test_data
            mock_refact.return_value = test_data
            
            original_result = original_tool.query_users(1)
            refactored_result = refactored_tool.query_users(1)
            
            assert original_result["success"] == refactored_result["success"]
            assert original_result["data"] == refactored_result["data"]
    
    def test_query_products_output_match(self, original_tool, refactored_tool):
        """Test that original and refactored query_products produce same output."""
        with patch.object(original_tool, '_execute_query') as mock_orig, \
             patch.object(refactored_tool, '_execute_raw_query') as mock_refact:
            
            test_data = [[1, "Widget", 19.99, 100]]
            mock_orig.return_value = test_data
            mock_refact.return_value = test_data
            
            original_result = original_tool.query_products(1)
            refactored_result = refactored_tool.query_products(1)
            
            assert original_result["success"] == refactored_result["success"]
            assert original_result["data"] == refactored_result["data"]
    
    def test_query_orders_output_match(self, original_tool, refactored_tool):
        """Test that original and refactored query_orders produce same output."""
        with patch.object(original_tool, '_execute_query') as mock_orig, \
             patch.object(refactored_tool, '_execute_raw_query') as mock_refact:
            
            test_data = [[1, 123, 99.99, "completed"]]
            mock_orig.return_value = test_data
            mock_refact.return_value = test_data
            
            original_result = original_tool.query_orders(1)
            refactored_result = refactored_tool.query_orders(1)
            
            assert original_result["success"] == refactored_result["success"]
            assert original_result["data"] == refactored_result["data"]
    
    def test_error_response_format_match(self, original_tool, refactored_tool):
        """Test that error responses have same format."""
        with patch.object(original_tool, '_execute_query') as mock_orig, \
             patch.object(refactored_tool, '_execute_raw_query') as mock_refact:
            
            mock_orig.return_value = None
            mock_refact.return_value = None
            
            original_result = original_tool.query_users(1)
            refactored_result = refactored_tool.query_users(1)
            
            assert original_result["success"] == refactored_result["success"]
            assert original_result["success"] is False
            assert original_result["data"] is None
            assert refactored_result["data"] is None
