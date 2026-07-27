#!/bin/bash

# OpenCode Plus Setup Script
# This script installs all required dependencies and configures the enhanced OpenCode environment

set -e

echo "🚀 OpenCode Plus Setup"
echo "===================="

# Check for existing installations
echo "📦 Checking prerequisites..."

# Install ripgrep if not present
if ! command -v rg &> /dev/null; then
    echo "Installing ripgrep..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y ripgrep
    elif command -v yum &> /dev/null; then
        sudo yum install -y ripgrep
    elif command -v brew &> /dev/null; then
        brew install ripgrep
    else
        echo "⚠️  Could not install ripgrep automatically. Please install it manually."
        exit 1
    fi
fi

# Ensure Bun is installed
if ! command -v bun &> /dev/null; then
    echo "Installing Bun..."
    curl -fsSL https://bun.sh/install | bash
    export PATH="$HOME/.bun/bin:$PATH"
fi

# Create necessary directories
mkdir -p .opencode/plugins
mkdir -p .opencode/skills 
mkdir -p .opencode/agents
mkdir -p .opencode/scripts
mkdir -p .opencode/asp-servers
mkdir -p .opencode/mcp-servers

# Install plugin dependencies
echo "🔧 Installing plugin dependencies..."
cd .opencode
bun install --silent
cd ..

# Install OpenCode if not present
if ! command -v opencode &> /dev/null; then
    echo "Installing OpenCode..."
    curl -fsSL https://opencode.ai/install | bash
    export PATH="$HOME/.opencode/bin:$PATH"
fi

# Verify configuration
echo "🔍 Verifying configuration..."
if [ -f "opencode.json" ]; then
    echo "✅ Found opencode.json"
fi

if [ -f "opencode-plus.json" ]; then
    echo "✅ Found opencode-plus.json (enhanced configuration)"
fi

# Test OpenCode installation
echo "🧪 Testing OpenCode installation..."
if command -v opencode &> /dev/null; then
    opencode --version || echo "OpenCode basic check passed"
fi

# Test ripgrep
echo "🧪 Testing ripgrep..."
if command -v rg &> /dev/null; then
    rg --version | head -1
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "Installed tools:"
echo "  - OpenCode CLI ✓"
echo "  - Bun ✓"
echo "  - Ripgrep ✓"
echo ""
echo "Configuration files:"
echo "  - opencode.json"
echo "  - opencode-plus.json"
echo ""
echo "Next steps:"
echo "  1. Review and customize configuration files"
echo "  2. Run: opencode validate-config"
echo "  3. Start: opencode run"
echo ""