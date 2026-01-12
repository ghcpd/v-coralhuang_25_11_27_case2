"""
Refactored Database Tool for AI Agent
Eliminates code duplication using generic query methods, parameterized SQL,
and config-driven field mapping.
"""
from typing import Dict, List, Any, Optional
from contextlib import contextmanager
from .base_tool import BaseTool


class DatabaseToolRefactored(BaseTool):
    """Refactored database tool with eliminated duplication and improved security."""
    
    # Configuration dictionary for query types
    QUERY_CONFIG = {
        "users": {
            "table": "users",
            "fields": ["id", "name", "email", "created_at"]
        },
        "products": {
            "table": "products",
            "fields": ["id", "name", "price", "stock"]
        },
        "orders": {
            "table": "orders",
            "fields": ["id", "user_id", "total", "status"]
        }
    }
    
    def __init__(self, connection_string: str):
        """
        Initialize database tool with connection string.
        
        Args:
            connection_string: Database connection string
        """
        super().__init__()
        self.connection_string = connection_string
    
    @contextmanager
    def _get_connection(self):
        """
        Context manager for database connections.
        Ensures proper connection cleanup.
        
        Yields:
            Database connection object
        """
        connection = None
        try:
            self._log_operation(f"Connecting to database: {self.connection_string}")
            connection = self._create_connection()
            
            if connection is None:
                raise ConnectionError("Failed to establish database connection")
            
            yield connection
        finally:
            if connection:
                connection.close()
                self._log_operation("Database connection closed", "debug")
    
    def _execute_query(self, query_type: str, entity_id: int) -> Dict[str, Any]:
        """
        Generic method to execute parameterized queries for any entity type.
        
        Args:
            query_type: Type of query (users, products, orders)
            entity_id: ID of the entity to query
        
        Returns:
            Standardized response dictionary
        """
        if query_type not in self.QUERY_CONFIG:
            return self.format_response(
                success=False,
                error=f"Invalid query type: {query_type}"
            )
        
        config = self.QUERY_CONFIG[query_type]
        table = config["table"]
        fields = config["fields"]
        
        with self._get_connection() as connection:
            # Use parameterized query to prevent SQL injection
            query = f"SELECT * FROM {table} WHERE id = ?"
            self._log_operation(f"Executing query: {query} with params: [{entity_id}]")
            
            result = self._execute_raw_query(connection, query, (entity_id,))
            
            if result is None:
                return self.format_response(
                    success=False,
                    error="Query execution failed"
                )
            
            # Process results using config-driven field mapping
            processed_data = self._process_results(result, fields)
            
            self._log_operation(f"Query successful, returned {len(processed_data)} rows")
            return self.format_response(success=True, data=processed_data)
    
    def _process_results(self, result: List[tuple], fields: List[str]) -> List[Dict[str, Any]]:
        """
        Process query results into dictionaries using field mapping.
        
        Args:
            result: Raw query result rows
            fields: List of field names in order
        
        Returns:
            List of dictionaries with named fields
        """
        processed_data = []
        for row in result:
            row_dict = {fields[i]: row[i] for i in range(len(fields))}
            processed_data.append(row_dict)
        return processed_data
    
    @BaseTool.handle_errors("database query")
    def query_users(self, user_id: int) -> Dict[str, Any]:
        """
        Query user data from database.
        
        Args:
            user_id: ID of the user to query
        
        Returns:
            Standardized response with user data
        """
        return self._execute_query("users", user_id)
    
    @BaseTool.handle_errors("database query")
    def query_products(self, product_id: int) -> Dict[str, Any]:
        """
        Query product data from database.
        
        Args:
            product_id: ID of the product to query
        
        Returns:
            Standardized response with product data
        """
        return self._execute_query("products", product_id)
    
    @BaseTool.handle_errors("database query")
    def query_orders(self, order_id: int) -> Dict[str, Any]:
        """
        Query order data from database.
        
        Args:
            order_id: ID of the order to query
        
        Returns:
            Standardized response with order data
        """
        return self._execute_query("orders", order_id)
    
    def _create_connection(self):
        """
        Create database connection (simulated).
        In production, this would use actual database drivers.
        
        Returns:
            Database connection object
        """
        class MockConnection:
            def close(self):
                pass
        return MockConnection()
    
    def _execute_raw_query(self, connection, query: str, params: tuple = None):
        """
        Execute raw query with parameters (simulated).
        In production, this would execute actual parameterized queries.
        
        Args:
            connection: Database connection object
            query: SQL query with parameter placeholders
            params: Tuple of parameter values
        
        Returns:
            Query result rows
        """
        # Simulated query execution
        return [[1, "Test", "test@example.com", "2024-01-01"]]
