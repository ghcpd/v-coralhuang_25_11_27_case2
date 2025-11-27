# Agent Tools Refactor

Quick start:

Windows:
 - .\setup_env.ps1; .\run_tests.ps1

Linux/macOS:
 - ./setup_env.sh; ./run_tests.sh

Before/After highlights:
- Code duplication reduced significantly by centralizing shared logic into `BaseTool` and generic methods (aim: ~80% reduction).
- Cyclomatic complexity lowered by consolidating repeated try/except and result parsing flows.
- Security: Parameterized queries prevent SQL injection risks.
- Test coverage: Includes unit and parity tests ensuring legacy and refactored output parity.

Testing:
- Run `.\setup_env.ps1` to create a venv and install deps on Windows.
- Run `.\run_tests.ps1` to execute the test suite with coverage.


Overview:
- `src/agent_tools/base_tool.py`: Shared utilities and decorator
- `src/agent_tools/database_tool_refactored.py`: Database tool refactor
- `src/agent_tools/api_tool_refactored.py`: API tool refactor
 - `tests/`: Unit tests and comparison tests

Design goal: Remove duplicated code, centralize error handling, parameterize SQL queries, and provide a one-command setup for new developers.
