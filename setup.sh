#!/bin/bash

# Terminal Color Theme Creator - Setup Script
# This script sets up the project using uv for dependency management

set -e

echo "🎨 Setting up Terminal Color Theme Creator with uv..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Add uv to PATH for current session
    source "$HOME/.cargo/env"
    echo "✅ uv installed successfully!"
else
    echo "✅ uv is already installed!"
fi

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Please run this script from the theme-viz directory!"
    exit 1
fi

# Install dependencies using uv
echo "📦 Installing dependencies..."
uv sync

echo "🎉 Setup complete!"
echo ""
echo "How to use:"
echo "  • GUI version:      uv run python main.py"
echo "  • Demo version:     uv run python demo.py"
echo "  • Test version:     uv run python test_theme_generator.py"
echo "  • Run as command:   theme-viz"
echo ""
echo "Note: The GUI version requires tkinter to be available on your system."
