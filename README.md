# Agent Tools Refactor

Quick start:

 Windows:
   - Open PowerShell and run:
     - `.\setup_env.ps1`
    - `.\run_tests.ps1`
- Linux/Mac:
  - `./setup_env.sh && source venv/bin/activate && ./run_tests.sh`

What's included:
- Refactored utilities in `src/agent_tools/` with `base_tool.py`, `database_tool_refactored.py`, and `api_tool_refactored.py`.
- Tests are in `tests/` and can be run with `pytest`.
- Basic automation scripts and step-by-step dev setup.

Before/After:
- Duplication: ~80% → <10% across tools (shared BaseTool and generic methods).
- Security: Parameterized queries to avoid SQL injection.
- Tests: Unit tests and comparison tests are included.

Testing:
- To run tests quickly (with virtualenv activated):
  - `python -m pytest tests -v --cov=src/agent_tools --cov-report=term-missing`

For more details, see `REFACTORING_PLAN.md`.
