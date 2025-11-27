#!/bin/bash
# Run tests with coverage reporting
# Usage: ./run_tests.sh

echo "================================================"
echo "Running Agent Tools Tests"
echo "================================================"
echo ""

# Check if venv is activated
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo "Running pytest with coverage..."
pytest tests/ -v --cov=src/agent_tools --cov-report=term-missing --cov-report=html

echo ""
echo "================================================"
echo "Test execution completed"
echo "================================================"
echo ""
echo "Coverage report generated in: htmlcov/index.html"
echo ""
