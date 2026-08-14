#!/bin/bash
set -e

# Force Python 3.11 (or use system python if available)
export PYTHON_VERSION=3.11

pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

echo "✅ Build complete - bot ready to run"
