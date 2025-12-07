#!/bin/bash
# Setup script for C++ tests

set -e  # Exit on error

echo "Setting up C++ PID Controller Tests"
echo "===================================="
echo ""

# Check if catch.hpp exists
if [ ! -f "catch.hpp" ]; then
    echo "Downloading Catch2 v2.13.10..."
    if command -v wget &> /dev/null; then
        wget -q https://github.com/catchorg/Catch2/releases/download/v2.13.10/catch.hpp
    elif command -v curl &> /dev/null; then
        curl -L -o catch.hpp https://github.com/catchorg/Catch2/releases/download/v2.13.10/catch.hpp
    else
        echo "Error: Neither wget nor curl found. Please install one of them."
        exit 1
    fi
    echo "✓ Downloaded catch.hpp"
else
    echo "✓ catch.hpp already exists"
fi

# Check if I/O data files exist
if [ ! -d "data" ] || [ -z "$(ls -A data 2>/dev/null)" ]; then
    echo ""
    echo "Generating I/O data files..."
    cd ..
    python3 tests/generate_io_data.py
    cd tests
    echo "✓ Generated I/O data files"
else
    echo "✓ I/O data files exist"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Build tests:     make"
echo "  2. Run tests:       make test"
echo "  3. Verbose output:  make test-verbose"
echo ""
echo "Or use VS Code:"
echo "  - Press Cmd+Shift+B to build"
echo "  - Press Cmd+Shift+P, type 'Tasks: Run Test Task'"
echo "  - Press F5 to debug tests"
