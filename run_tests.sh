#!/bin/bash

# Test runner script for All The Content modpack
# This script runs all test suites and generates a summary report

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================================"
echo "  All The Content - Modpack Test Suite"
echo "================================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Get Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"
echo ""

# Navigate to repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Run tests with verbose output
echo -e "${YELLOW}Running test suite...${NC}"
echo ""

# Run all tests
if python3 -m unittest discover tests -v; then
    echo ""
    echo -e "${GREEN}================================================${NC}"
    echo -e "${GREEN}  All tests passed successfully!${NC}"
    echo -e "${GREEN}================================================${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}================================================${NC}"
    echo -e "${RED}  Some tests failed!${NC}"
    echo -e "${RED}================================================${NC}"
    exit 1
fi
