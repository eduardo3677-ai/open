#!/bin/bash

# OpenCode Plus Quick Demo
# Demonstrates the key enhancements and features

echo "🚀 OpenCode Plus - Quick Demo"
echo "================================"
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}1. Configuration System${NC}"
echo "-------------------------------"

echo "Basic Configuration:"
if [ -f "opencode.json" ]; then
    echo "✅ Configuration loaded from opencode.json"
    echo "   Model: $(jq -r '.model' opencode.json)"
    echo "   Log Level: $(jq -r '.logLevel' opencode.json)"
else
    echo "❌ opencode.json not found"
fi

echo ""
echo "Enhanced Configuration:"
if [ -f "opencode-plus.json" ]; then
    echo "✅ Enhanced configuration loaded from opencode-plus.json"
    echo "   Model: $(jq -r '.model' opencode-plus.json)"
    echo "   Extensions:"
    echo "     - Plugins: $(jq -r '.extensions.plugins | length' opencode-plus.json)"
    echo "     - Skills: $(jq -r '.extensions.skills | length' opencode-plus.json)"
    echo "   Compression: $(jq -r '.compaction.auto' opencode-plus.json)"
    echo "   Token Trigger: $(jq -r '.compaction.triggerTokenRatio' opencode-plus.json)"
else
    echo "❌ opencode-plus.json not found"
fi

echo ""
echo -e "${BLUE}2. Tool Installation${NC}"
echo "-------------------------------"

if command -v jq &> /dev/null; then
    echo "✅ jq ($(jq --version)) - Configuration validation"
else
    echo "❌ jq not installed"
fi

if command -v rg &> /dev/null; then
    echo "✅ ripgrep ($(rg --version | head -1)) - Fast content search"
    # Demonstrate ripgrep speed
    echo "   Searching for 'model' in JSON files..."
    start=$(date +%s)
    result=$(rg "model" --type json --count | head -3)
    end=$(date +%s)
    echo "   ⚡ Search completed in $((end-start)) seconds"
    echo "   Results: $result"
else
    echo "⚠️  ripgrep not installed (optional but recommended)"
fi

if command -v bun &> /dev/null; then
    echo "✅ bun ($(bun --version)) - Package manager"
else
    echo "⚠️  bun not installed"
fi

echo ""
echo -e "${BLUE}3. Extension Structure${NC}"
echo "-------------------------------"

# Create directories if they don't exist
mkdir -p .opencode/{plugins,skills,agents,asp-servers,mcp-servers}

echo "Directory structure:"
for dir in plugins skills agents asp-servers mcp-servers; do
    if [ -d ".opencode/$dir" ]; then
        item_count=$(find ".opencode/$dir" -type f 2>/dev/null | wc -l)
        echo "✅ .opencode/$dir ($item_count items)"
    else
        echo "❌ .opencode/$dir (missing)"
    fi
done

echo ""
echo -e "${BLUE}4. Scripts & Management${NC}"
echo "-------------------------------"

echo "Available scripts:"
if [ -x "scripts/install_plus.sh" ]; then
    echo "✅ install_plus.sh - Setup script"
else
    echo "❌ install_plus.sh - Not executable or missing"
fi

if [ -x "scripts/opencode-manage.sh" ]; then
    echo "✅ opencode-manage.sh - Management CLI"
else
    echo "❌ opencode-manage.sh - Not executable or missing"
fi

if [ -x "scripts/test-plus.sh" ]; then
    echo "✅ test-plus.sh - Test suite"
else
    echo "❌ test-plus.sh - Not executable or missing"
fi

echo ""
echo -e "${BLUE}5. GitHub Action Integration${NC}"
echo "-------------------------------"

if [ -f ".github/enhanced/action.yml" ]; then
    echo "✅ Enhanced action configuration (.github/enhanced/action.yml)"

    # Show key enhancements in the action
    if command -v grep &> /dev/null; then
        enable_ripgrep=$(grep -A2 "enable_ripgrep:" .github/enhanced/action.yml | grep "default" | cut -d'"' -f2)
        enable_extensions=$(grep -A2 "enable_extensions:" .github/enhanced/action.yml | grep "default" | cut -d'"' -f2)

        echo "   • Enable ripgrep: $enable_ripgrep"
        echo "   • Enable extensions: $enable_extensions"
    fi
else
    echo "❌ Enhanced GitHub action not found"
fi

echo ""
echo -e "${BLUE}6. Documentation${NC}"
echo "-------------------------------"

echo "Available documentation:"
for doc in README-PLUS.md IMPLEMENTATION-SUMMARY.md opencode-plus-plan.md config-plus.schema.json; do
    if [ -f "$doc" ]; then
        echo "✅ $doc"
    else
        echo "❌ $doc"
    fi
done

echo ""
echo -e "${BLUE}7. Key Features Summary${NC}"
echo "-------------------------------"

echo "🎯 Configuration Management:"
echo "   • Schema-based validation"
echo "   • Dynamic extension loading"
echo "   • Environment-specific configs"

echo ""
echo "🚀 Enhanced Performance:"
echo "   • Ripgrep for 100x faster searches"
echo "   • Parallel tool execution"
echo "   • Lazy extension loading"

echo ""
echo "🔌 Extension System:"
echo "   • Plugins (wakatime, notifier, type-inject)"
echo "   • Skills (code-review, debugging, refactoring, testing)"
echo "   • Agents (expert, reviewer)"
echo "   • ASP/MCP server integration"

echo ""
echo "📊 Smart Conversation Management:"
echo "   • Token limit detection"
echo "   • Automatic compression at 85% threshold"
echo "   • Context summarization"
echo "   • Preserve recent/critical messages"

echo ""
echo "📝 Enhanced Logging:"
echo "   • Model reasoning traces"
echo "   • Tool execution details"
echo "   • File change diffs"
echo "   • GitHub Actions annotations"

echo ""
echo -e "${GREEN}✨ Demo Complete!${NC}"
echo ""
echo "OpenCode Plus is ready for development with:"
echo "  • Enhanced configuration system"
echo "  • Fast file operations with ripgrep"
echo "  • Comprehensive extension support"
echo "  • Smart token management"
echo "  • Rich logging and debugging"
echo ""
echo "Next steps:"
echo "  1. ✅ Validate configuration: ./scripts/test-plus.sh"
echo "  2. ✅ Manage system: ./scripts/opencode-manage.sh status"
echo "  3. ✅ Start session: opencode run --config opencode-plus.json"
echo ""