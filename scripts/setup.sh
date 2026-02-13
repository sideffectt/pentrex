#!/bin/bash
set -e

echo "Setting up Pentrex..."

# Create venv
python3 -m venv venv
source venv/bin/activate

# Install
pip install -e ".[all]"

# Create .env if not exists
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env — add your API key"
fi

# Create loot dir
mkdir -p loot

echo ""
echo "Setup complete! Run:"
echo "  source venv/bin/activate"
echo "  pentrex"
