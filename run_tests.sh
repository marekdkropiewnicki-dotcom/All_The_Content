#!/bin/bash
# Quick test runner script for All The Content modpack

echo "=================================="
echo "All The Content - Test Suite"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.6 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"
echo ""

# Run the tests
echo "Running tests..."
echo ""

python -m unittest discover tests -v

# Capture exit code
TEST_EXIT_CODE=$?

echo ""
echo "=================================="
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed. Please review the output above."
fi
echo "=================================="

exit $TEST_EXIT_CODE
