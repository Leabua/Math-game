#!/bin/bash
# MathPy GUI Installation Script
# Handles pygame-ce vs pygame conflict for Python 3.14

echo "Installing MathPy GUI dependencies..."

# Create venv if needed
if [ ! -d ".venv" ]; then
    python -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# IMPORTANT: Uninstall any existing pygame packages first
pip uninstall pygame pygame-ce pygame-chart -y 2>/dev/null

# Install pygame-ce FIRST (required for Python 3.14 compatibility)
pip install pygame-ce

# Install pygame-chart WITHOUT dependencies (it tries to install pygame which breaks)
pip install pygame-chart --no-deps

echo "Installation complete!"
echo "Run: .venv/bin/python gui/main.py"
