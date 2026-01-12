#!/bin/bash
# Run Tests Script (Bash)
# Activates virtual environment and runs pytest with coverage

echo "=== Running Tests ==="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "✗ Virtual environment not found. Please run setup_env.sh first."
    exit 1
fi

# Activate virtual environment
echo -e "\nActivating virtual environment..."
source venv/bin/activate

# Run tests with coverage
echo -e "\nRunning tests with coverage..."
echo "============================================================"

pytest tests/ -v --cov=src/agent_tools --cov-report=term-missing --cov-report=html

exitCode=$?

echo "============================================================"

if [ $exitCode -eq 0 ]; then
    echo -e "\n✓ All tests passed!"
    echo -e "\nCoverage report saved to: htmlcov/index.html"
else
    echo -e "\n✗ Some tests failed"
    exit $exitCode
fi
