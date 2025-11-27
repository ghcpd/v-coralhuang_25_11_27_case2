#!/bin/bash
# Setup environment script for Linux/macOS
# Checks Python 3.8+, creates venv, and installs dependencies

set -e  # Exit on error

echo "================================================"
echo "Agent Tools Refactoring - Environment Setup"
echo "================================================"

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Verify Python 3.8+
python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" || {
    echo "Error: Python 3.8 or higher is required"
    exit 1
}

echo "✓ Python version check passed"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "✓ pip upgraded"

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Production dependencies installed"

echo "Installing dev dependencies..."
pip install -q -r requirements-dev.txt
echo "✓ Development dependencies installed"

echo ""
echo "================================================"
echo "✓ Environment setup completed successfully!"
echo "================================================"
echo ""
echo "To activate the environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run tests, use:"
echo "  ./run_tests.sh"
echo ""
