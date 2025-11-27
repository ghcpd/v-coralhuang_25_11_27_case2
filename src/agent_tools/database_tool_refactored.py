"""
Database Tool for AI Agent - Refactored
Handles database query operations with DRY principles and parameterized queries
"""
from contextlib import contextmanager
from typing import Dict, Any, List, Optional
import logging

from base_tool import BaseTool


class DatabaseToolRefactored(BaseTool):
    """Refactored database tool using generic query method and config-driven approach"""
    
    # Configuration for different entity types
    QUERY_CONFIG = {
        "users": {
            "table": "users",
            "fields": ["id", "name", "email", "created_at"],
            "field_mapping": {
                "id": "id",
                "name": "name",
                "email": "email",
                "created_at": "created_at"
            }
        },
        "products": {
            "table": "products",
            "fields": ["id", "name", "price", "stock"],
            "field_mapping": {
                "id": "id",
                "name": "name",
                "price": "price",
                "stock": "stock"
            }
        },
        "orders": {
            "table": "orders",
            "fields": ["id", "user_id", "total", "status"],
            "field_mapping": {
                "id": "id",
                "user_id": "user_id",
                "total": "total",
                "status": "status"
            }
        }
    }
    
    def __init__(self, connection_string: str):
        """Initialize DatabaseToolRefactored"""
        super().__init__(logger_name=__name__)
        self.connection_string = connection_string
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections"""
        self.logger.info(f"Connecting to database: {self.connection_string}")
        connection = self._create_connection()
        
        if connection is None:
            self.logger.error("Failed to create database connection")
            raise ConnectionError("Database connection failed")
        
        try:
            yield connection
        finally:
            self._close_connection(connection)
            self.logger.debug("Database connection closed")
    
    def _execute_query(self, query_type: str, entity_id: int) -> Dict[str, Any]:
        """
        Generic query execution method - eliminates duplication
        
        Args:
            query_type: Type of query (users, products, orders)
            entity_id: ID of entity to query
            
        Returns:
            Formatted response with query results
        """
        if query_type not in self.QUERY_CONFIG:
            return self.format_response(
                success=False,
                error=f"Unknown query type: {query_type}",
                data=None
            )
        
        try:
            config = self.QUERY_CONFIG[query_type]
            table = config["table"]
            field_mapping = config["field_mapping"]
            
            with self._get_connection() as connection:
                # Use parameterized query to prevent SQL injection
                query = f"SELECT * FROM {table} WHERE id = ?"
                self.logger.info(f"Executing parameterized query on {table}")
                
                result = self._execute(connection, query, (entity_id,))
                
                if result is None:
                    return self.format_response(
                        success=False,
                        error="Query execution failed",
                        data=None
                    )
                
                # Process result using field mapping
                processed_data = []
                for row in result:
                    entity_dict = {}
                    for idx, field_name in enumerate(config["fields"]):
                        entity_dict[field_mapping[field_name]] = row[idx]
                    processed_data.append(entity_dict)
                
                self.logger.info(f"Query successful, returned {len(processed_data)} rows")
                return self.format_response(
                    success=True,
                    data=processed_data,
                    error=None
                )
        
        except ConnectionError as e:
            self.logger.error(f"Connection error: {str(e)}")
            return self.format_response(
                success=False,
                error=str(e),
                data=None
            )
        except Exception as e:
            self.logger.error(f"Error executing query: {str(e)}")
            return self.format_response(
                success=False,
                error=str(e),
                data=None
            )
    
    def query_users(self, user_id: int) -> Dict[str, Any]:
        """Query user data from database"""
        return self._execute_query("users", user_id)
    
    def query_products(self, product_id: int) -> Dict[str, Any]:
        """Query product data from database"""
        return self._execute_query("products", product_id)
    
    def query_orders(self, order_id: int) -> Dict[str, Any]:
        """Query order data from database"""
        return self._execute_query("orders", order_id)
    
    def _create_connection(self):
        """Simulated database connection"""
        # In real implementation, this would create actual DB connection
        from unittest.mock import Mock
        mock_conn = Mock()
        mock_conn.status = "connected"
        return mock_conn
    
    def _close_connection(self, connection):
        """Close database connection"""
        if connection and hasattr(connection, 'close'):
            connection.close()
    
    def _execute(self, connection, query: str, params: tuple = None):
        """Simulated query execution with parameterization support"""
        # In real implementation, this would execute actual query with parameterized values
        # For simulation, we return consistent test data
        if "users" in query:
            return [[1, "Test", "test@example.com", "2024-01-01"]]
        elif "products" in query:
            return [[1, "Test Product", 99.99, 10]]
        elif "orders" in query:
            return [[1, 1, 199.99, "completed"]]
        return None
