"""
Tests for DatabaseToolRefactored
Tests generic query execution, parameterized SQL, and config-driven approach
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'agent_tools'))

from database_tool_refactored import DatabaseToolRefactored
from database_tool import DatabaseTool


class TestDatabaseToolRefactored:
    """Test suite for DatabaseToolRefactored class"""
    
    @pytest.fixture
    def db_tool_refactored(self):
        """Create DatabaseToolRefactored instance for testing"""
        return DatabaseToolRefactored("test_connection_string")
    
    @pytest.fixture
    def db_tool_original(self):
        """Create original DatabaseTool instance for comparison"""
        return DatabaseTool("test_connection_string")
    
    def test_query_users_success(self, db_tool_refactored):
        """Test successful user query"""
        result = db_tool_refactored.query_users(1)
        
        assert result["success"] is True
        assert result["error"] is None
        assert isinstance(result["data"], list)
        assert len(result["data"]) > 0
        assert "id" in result["data"][0]
        assert "name" in result["data"][0]
    
    def test_query_products_success(self, db_tool_refactored):
        """Test successful product query"""
        result = db_tool_refactored.query_products(1)
        
        assert result["success"] is True
        assert result["error"] is None
        assert isinstance(result["data"], list)
        assert len(result["data"]) > 0
        assert "id" in result["data"][0]
        assert "price" in result["data"][0]
    
    def test_query_orders_success(self, db_tool_refactored):
        """Test successful order query"""
        result = db_tool_refactored.query_orders(1)
        
        assert result["success"] is True
        assert result["error"] is None
        assert isinstance(result["data"], list)
        assert len(result["data"]) > 0
        assert "id" in result["data"][0]
        assert "status" in result["data"][0]
    
    @pytest.mark.parametrize("query_type,entity_id", [
        ("users", 1),
        ("products", 1),
        ("orders", 1)
    ])
    def test_execute_query_all_types(self, db_tool_refactored, query_type, entity_id):
        """Test generic _execute_query method with all entity types"""
        result = db_tool_refactored._execute_query(query_type, entity_id)
        
        assert result["success"] is True
        assert result["error"] is None
        assert result["data"] is not None
    
    def test_execute_query_invalid_type(self, db_tool_refactored):
        """Test _execute_query with invalid query type"""
        result = db_tool_refactored._execute_query("invalid", 1)
        
        assert result["success"] is False
        assert "Unknown query type" in result["error"]
        assert result["data"] is None
    
    def test_context_manager_connection(self, db_tool_refactored):
        """Test context manager properly handles connections"""
        with patch.object(db_tool_refactored, '_create_connection') as mock_conn:
            with patch.object(db_tool_refactored, '_close_connection') as mock_close:
                mock_conn.return_value = {"status": "connected"}
                
                with db_tool_refactored._get_connection() as conn:
                    assert conn["status"] == "connected"
                
                mock_close.assert_called_once()
    
    def test_context_manager_connection_failure(self, db_tool_refactored):
        """Test context manager with connection failure"""
        with patch.object(db_tool_refactored, '_create_connection') as mock_conn:
            mock_conn.return_value = None
            
            with pytest.raises(ConnectionError):
                with db_tool_refactored._get_connection():
                    pass
    
    def test_field_mapping_users(self, db_tool_refactored):
        """Test correct field mapping for users"""
        result = db_tool_refactored.query_users(1)
        user = result["data"][0]
        
        # Verify expected fields are mapped correctly
        expected_fields = ["id", "name", "email", "created_at"]
        for field in expected_fields:
            assert field in user
    
    def test_field_mapping_products(self, db_tool_refactored):
        """Test correct field mapping for products"""
        result = db_tool_refactored.query_products(1)
        product = result["data"][0]
        
        # Verify expected fields are mapped correctly
        expected_fields = ["id", "name", "price", "stock"]
        for field in expected_fields:
            assert field in product
    
    def test_field_mapping_orders(self, db_tool_refactored):
        """Test correct field mapping for orders"""
        result = db_tool_refactored.query_orders(1)
        order = result["data"][0]
        
        # Verify expected fields are mapped correctly
        expected_fields = ["id", "user_id", "total", "status"]
        for field in expected_fields:
            assert field in order
    
    @pytest.mark.parametrize("method_name,entity_id", [
        ("query_users", 1),
        ("query_products", 1),
        ("query_orders", 1)
    ])
    def test_all_query_methods(self, db_tool_refactored, method_name, entity_id):
        """Test all public query methods work correctly"""
        method = getattr(db_tool_refactored, method_name)
        result = method(entity_id)
        
        assert result["success"] is True
        assert result["data"] is not None
    
    def test_comparison_original_vs_refactored_structure(self, db_tool_original, db_tool_refactored):
        """Test that refactored tool returns same structure as original"""
        # Both should have same top-level structure
        original_result = db_tool_original.query_users(1)
        refactored_result = db_tool_refactored.query_users(1)
        
        assert set(original_result.keys()) == set(refactored_result.keys())
        assert original_result["success"] == refactored_result["success"]
        assert type(original_result["data"]) == type(refactored_result["data"])
    
    def test_query_config_completeness(self, db_tool_refactored):
        """Test that QUERY_CONFIG has all required entity types"""
        required_types = ["users", "products", "orders"]
        for entity_type in required_types:
            assert entity_type in db_tool_refactored.QUERY_CONFIG
            config = db_tool_refactored.QUERY_CONFIG[entity_type]
            assert "table" in config
            assert "fields" in config
            assert "field_mapping" in config
    
    def test_parameterized_query_usage(self, db_tool_refactored):
        """Test that parameterized queries are used (no f-string SQL injection risk)"""
        with patch.object(db_tool_refactored, '_execute') as mock_execute:
            mock_execute.return_value = [[1, "Test", "test@example.com", "2024-01-01"]]
            
            db_tool_refactored.query_users(1)
            
            # Verify parameterized query (second arg should be tuple with ID)
            mock_execute.assert_called_once()
            call_args = mock_execute.call_args
            assert call_args[0][1] == "SELECT * FROM users WHERE id = ?"
            assert call_args[0][2] == (1,)
