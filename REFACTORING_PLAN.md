# REFACTORING PLAN

Goal
- Eliminate duplication, improve clarity, and add tests. Preserve original functionality.

Design
- Extract BaseTool (Template Method + Decorator patterns) with shared response formatter and error decorator.
- DatabaseToolRefactored: generic `_execute_query(entity, entity_id)` with config-driven fields; context manager for connections; parameterized queries.
- APIToolRefactored: generic `_make_request(path, params)` with centralized headers, timeout, error handling.

Testing Strategy
- Unit tests for BaseTool utilities and decorator
- Unit tests for DatabaseToolRefactored and APIToolRefactored using patching/mocking of _execute and requests.get
- Comparison tests that verify original and refactored outputs match for identical inputs

Success Metrics
- Reduce duplication to <10%
- Unit tests cover core logic and all branches (success, error, timeout)
- One-command setup to run tests on both PowerShell and Bash

Implementation Notes
- Parameterized SQL uses `?` placeholder for DB API compatibility
- The `_execute` method is designed to be patched in tests to simulate DB responses
- The design should allow easy migration to actual DB drivers (sqlite/psycopg2) by replacing `_create_connection` and `_execute` implementations

