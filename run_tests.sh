#!/bin/bash
# Test runner script for All The Content modpack

set -e  # Exit on error

echo "==================================="
echo "Running All The Content Test Suite"
echo "==================================="
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed"
    exit 1
fi

# Run tests with verbose output
echo "Running tests with Python unittest..."
echo ""

# Run all tests
python3 -m unittest discover tests -v

# Capture exit code
TEST_EXIT_CODE=$?

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "==================================="
    echo "✓ All tests passed successfully!"
    echo "==================================="
else
    echo "==================================="
    echo "✗ Some tests failed"
    echo "==================================="
fi

exit $TEST_EXIT_CODE
