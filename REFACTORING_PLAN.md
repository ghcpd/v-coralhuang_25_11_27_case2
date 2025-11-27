# Refactoring Plan

Problem analysis:
- The original code in `database_tool.py` and `api_tool.py` repeated connection setup, error handling, and response formatting across multiple methods. This created large duplication and increased maintenance costs.

Design Goals:
- Extract shared behavior to `BaseTool` (formatting, error handling, logger) - Decorator-based error wrapper.
- Implement generic query/request functions with configuration to remove duplicated logic.
- Use parameterized queries and simulated connection context manager to avoid SQL injection risks.
- Provide automated test structure using `pytest` and mocking.

Success Metrics:
- Duplication reduced by >70%.
- Tests cover success and error cases for DB and API tooling.
- One-command setup for Windows and Bash.

Implementation steps:
1. Create `BaseTool` with `format_response` and `handle_errors`.
2. Replace repeated database logic with `DatabaseToolRefactored` using a single `_execute` delegator.
3. Replace repeated API logic with `APIToolRefactored` using `_make_request` and `_get_headers`.
4. Add tests and automation scripts.
