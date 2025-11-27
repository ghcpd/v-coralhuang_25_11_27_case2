# Refactoring Plan

## Problems Identified
- ~80% duplicated code across `database_tool.py` and `api_tool.py` (logging, error handling, response shaping).
- SQL injection risk via string interpolation in queries.
- Mixed concerns: business logic interwoven with logging and error handling.
- Maintainability cost: changing error format required edits in 6+ locations.

## Design Goals
- DRY utilities for response formatting, logging, and error handling.
- Template methods for DB queries and API requests.
- Config-driven schemas/endpoints for flexibility.
- Safe DB access via parameterized queries and context-managed connections.
- Comprehensive, fast unit tests with mocks/fixtures; comparison against originals.

## Architecture & Patterns
- **BaseTool**: shared `format_response()` + `@error_handler` decorator.
- **DatabaseToolRefactored**:
  - Template method `_execute_query(type, id)`.
  - `DB_CONFIG` strategy map for tables and fields.
  - Context manager for connections; parameterized `WHERE id = ?`.
- **APIToolRefactored**:
  - Template method `_make_request(key, value)`.
  - `API_CONFIG` strategy map for endpoints/params.
  - Centralized headers, unified error handling.

## Success Metrics
- Duplication <10% (shared utilities + configs).
- Cyclomatic complexity per public method cut by >50%.
- No f-string SQL; parameterized queries validated in tests.
- Test suite covers base, API, DB tools; original vs refactored outputs match under mocks.
- One-command setup & test for Windows/Linux.

## Implementation Steps
1. Create `base_tool.py` with response formatting and error decorator.
2. Refactor DB tool into `DatabaseToolRefactored` (generic query, config-driven, parameterized SQL).
3. Refactor API tool into `APIToolRefactored` (generic request, centralized headers).
4. Write pytest suites (fixtures, mocks, parametrization, comparison tests).
5. Add automation scripts, pytest config, dev requirements, and gitignore.
6. Document quick start, before/after metrics, and design rationale.
