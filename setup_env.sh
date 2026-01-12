#!/bin/bash
# Setup Python Environment Script (Bash)
# Checks Python version, creates virtual environment, and installs dependencies

echo "=== Python Environment Setup ==="

# Check Python version
echo -e "\nChecking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo "Found: $PYTHON_VERSION"
    
    # Extract version numbers
    VERSION=$(echo $PYTHON_VERSION | grep -oP '\d+\.\d+')
    MAJOR=$(echo $VERSION | cut -d. -f1)
    MINOR=$(echo $VERSION | cut -d. -f2)
    
    if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 8 ]; then
        echo "✓ Python 3.8+ detected"
    else
        echo "✗ Python 3.8+ required. Found: Python $MAJOR.$MINOR"
        exit 1
    fi
else
    echo "✗ Python not found. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment
echo -e "\nCreating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Removing old environment..."
    rm -rf venv
fi

python3 -m venv venv
if [ $? -eq 0 ]; then
    echo "✓ Virtual environment created"
else
    echo "✗ Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo -e "\nActivating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo -e "\nUpgrading pip..."
python -m pip install --upgrade pip

# Install requirements
echo -e "\nInstalling production dependencies..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ Production dependencies installed"
else
    echo "✗ Failed to install production dependencies"
    exit 1
fi

echo -e "\nInstalling development dependencies..."
pip install -r requirements-dev.txt
if [ $? -eq 0 ]; then
    echo "✓ Development dependencies installed"
else
    echo "✗ Failed to install development dependencies"
    exit 1
fi

# Summary
echo -e "\n=== Setup Complete ==="
echo "✓ Python environment ready"
echo -e "\nTo activate the environment manually, run:"
echo "  source venv/bin/activate"
echo -e "\nTo run tests, execute:"
echo "  ./run_tests.sh"
