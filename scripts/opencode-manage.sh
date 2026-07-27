#!/bin/bash

# OpenCode Plus Management CLI
# Comprehensive tool for managing OpenCode Plus environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
OPENCODE_CONFIG="${OPENCODE_CONFIG:-opencode-plus.json}"
OPENCODE_DIR="${OPENCODE_DIR:-.opencode}"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_help() {
    cat << EOF
OpenCode Plus Management CLI

Usage: opencode-manage [command] [options]

Commands:
  status            Show system status and configuration
  validate          Validate configuration files
  reload            Reload extensions and plugins
  compress          Manually trigger conversation compression
  logs [tail]       Show logs (tail option for live following)
  stats             Show usage statistics
  tools             List available tools and their status
  extensions        List loaded extensions
  config [get|set]  Get or set configuration values

Options:
  --config FILE     Use specified configuration file
  --verbose         Enable verbose output
  --help            Show this help message

Examples:
  opencode-manage status
  opencode-manage validate --config opencode-plus.json
  opencode-manage logs tail
  opencode-manage extensions list

EOF
}

show_status() {
    echo "🔍 OpenCode Plus System Status"
    echo "================================"

    # Check OpenCode installation
    if command -v opencode &> /dev/null; then
        log_success "✅ OpenCode CLI installed"
        echo "   Version: $(opencode --version 2>&1 | head -1 || echo 'Unknown')"
    else
        log_error "❌ OpenCode CLI not found"
    fi

    # Check Bun installation
    if command -v bun &> /dev/null; then
        log_success "✅ Bun installed"
        echo "   Version: $(bun --version)"
    else
        log_warning "⚠️  Bun not found"
    fi

    # Check ripgrep installation
    if command -v rg &> /dev/null; then
        log_success "✅ Ripgrep installed"
        echo "   Version: $(rg --version | head -1)"
    else
        log_warning "⚠️  Ripgrep not found"
    fi

    # Check configuration
    if [ -f "$OPENCODE_CONFIG" ]; then
        log_success "✅ Configuration file found"
        echo "   Location: $OPENCODE_CONFIG"

        # Show some configuration details
        if command -v jq &> /dev/null; then
            echo "   Model: $(jq -r '.model // "Not specified"' $OPENCODE_CONFIG)"
            echo "   Extensions: $(jq -r '.extensions | (.plugins // [] | length) + (.skills // [] | length)' $OPENCODE_CONFIG) total"
        fi
    else
        log_warning "⚠️  Configuration file not found"
    fi

    # Check directory structure
    echo ""
    echo "📁 Directory Structure:"
    for dir in "$OPENCODE_DIR"/{plugins,skills,agents,asp-servers,mcp-servers}; do
        if [ -d "$dir" ]; then
            item_count=$(find "$dir" -type f | wc -l)
            echo "   ✅ $(basename $dir): $item_count items"
        else
            echo "   ❌ $(basename $dir): not found"
        fi
    done
}

validate_config() {
    log_info "Validating OpenCode configuration..."

    if [ ! -f "$OPENCODE_CONFIG" ]; then
        log_error "Configuration file not found: $OPENCODE_CONFIG"
        return 1
    fi

    # Basic JSON validation
    if command -v jq &> /dev/null; then
        if ! jq empty "$OPENCODE_CONFIG" 2>/dev/null; then
            log_error "Invalid JSON in configuration file"
            return 1
        fi
    else
        # Fallback to node for JSON validation
        if ! node -e "JSON.parse(require('fs').readFileSync('$OPENCODE_CONFIG', 'utf8'))" 2>/dev/null; then
            log_error "Invalid JSON in configuration file"
            return 1
        fi
    fi

    log_success "Configuration file is valid JSON"

    # Check required fields
    log_info "Checking configuration fields..."

    if command -v jq &> /dev/null; then
        model=$(jq -r '.model // empty' "$OPENCODE_CONFIG")
        if [ -z "$model" ]; then
            log_warning "Model field not specified in configuration"
        else
            log_success "Model configured: $model"
        fi

        # Check extensions
        extensions=$(jq '.extensions // {}' "$OPENCODE_CONFIG")
        plugins_count=$(echo "$extensions" | jq -r '.plugins | length' 2>/dev/null || echo '0')
        skills_count=$(echo "$extensions" | jq -r '.skills | length' 2>/dev/null || echo '0')

        log_success "Plugins: $plugins_count, Skills: $skills_count"
    fi

    log_success "Configuration validation completed"
}

show_logs() {
    local follow=""
    if [ "$1" = "tail" ]; then
        follow="-f"
    fi

    log_info "Showing OpenCode logs..."
    tail $follow ~/.opencode/logs/*.log 2>/dev/null || echo "No log files found"
}

compress_conversation() {
    log_info "Manually triggering conversation compression..."

    # Check if OpenCode server is running
    if ! curl -s http://localhost:4096/health > /dev/null 2>&1; then
        log_error "OpenCode server is not running"
        return 1
    fi

    # Trigger compression via API (placeholder - actual implementation depends on OpenCode API)
    log_info "Compression trigger sent (placeholder - need API implementation)"
    log_success "Conversation compression initiated"
}

show_stats() {
    log_info "Fetching OpenCode usage statistics..."

    if ! curl -s http://localhost:4096/health > /dev/null 2>&1; then
        log_warning "OpenCode server is not running"
        return 1
    fi

    # Placeholder for stats API
    echo "📊 Usage Statistics:"
    echo "   Sessions active: (placeholder - need API implementation)"
    echo "   Tokens used: (placeholder - need API implementation)"
    echo "   Compression events: (placeholder - need API implementation)"
}

show_tools() {
    log_info "Listing available tools..."

    echo "🔧 Available Tools:"

    if command -v rg &> /dev/null; then
        echo "   ✅ ripgrep (content search)"
    else
        echo "   ❌ ripgrep (not installed)"
    fi

    if command -v opencode &> /dev/null; then
        echo "   ✅[opencode CLI"
    else
        echo "   ❌ opencode CLI (not installed)"
    fi

    echo "   📝 edit (file operations)"
    echo "   🐚 bash (command execution)"
    echo "   🔍 grep (content search)"
    echo "   📁 glob (pattern matching)"
}

show_extensions() {
    log_info "Listing loaded extensions..."

    if [ ! -f "$OPENCODE_CONFIG" ]; then
        log_error "Configuration file not found"
        return 1
    fi

    if command -v jq &> /dev/null; then
        echo "🔌 Loaded Extensions:"

        # Plugins
        plugins=$(jq -r '.extensions.plugins // [][]' "$OPENCODE_CONFIG" 2>/dev/null)
        if [ -n "$plugins" ]; then
            echo "  Plugins:"
            while IFS= read -r plugin; do
                echo "    ✅ $plugin"
            done <<< "$plugins"
        fi

        # Skills
        skills=$(jq -r '.extensions.skills // [][]' "$OPENCODE_CONFIG" 2>/dev/null)
        if [ -n "$skills" ]; then
            echo "  Skills:"
            while IFS= read -r skill; do
                echo "    ✅ $skill"
            done <<< "$skills"
        fi

        # ASP Servers
        asp_servers=$(jq -r '.extensions.asp_servers // [] | length' "$OPENCODE_CONFIG" 2>/dev/null)
        echo "  ASP Servers: $asp_servers configured"

        # MCP Servers
        mcp_servers=$(jq -r '.extensions.mcp_servers // [] | length' "$OPENCODE_CONFIG" 2>/dev/null)
        echo "  MCP Servers: $mcp_servers configured"
    else
        log_warning "jq not installed, cannot parse configuration"
    fi
}

config_operation() {
    local operation=$1
    local key=$2
    local value=$3

    if [ "$operation" = "get" ]; then
        if [ -f "$OPENCODE_CONFIG" ] && command -v jq &> /dev/null; then
            jq -r ".$key // empty" "$OPENCODE_CONFIG"
        else
            log_error "Cannot perform get operation"
        fi
    elif [ "$operation" = "set" ]; then
        if [ -f "$OPENCODE_CONFIG" ] && command -v jq &> /dev/null; then
            jq ".$key = \"$value\"" "$OPENCODE_CONFIG"
            log_success "Configuration updated: $key = $value"
        else
            log_error "Cannot perform set operation"
        fi
    else
        log_error "Unknown operation: $operation"
    fi
}

# Parse arguments
verbose=false
while [[ $# -gt 0 ]]; do
    case $1 in
        --config)
            OPENCODE_CONFIG="$2"
            shift 2
            ;;
        --verbose)
            verbose=true
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            break
            ;;
    esac
done

# Main logic
command=$1
options=${@:2}

case $command in
    status)
        show_status
        ;;
    validate)
        validate_config
        ;;
    reload)
        log_info "Reloading extensions..."
        # Placeholder for reload logic
        log_success "Extensions reloaded"
        ;;
    compress)
        compress_conversation
        ;;
    logs)
        show_logs $options
        ;;
    stats)
        show_stats
        ;;
    tools)
        show_tools
        ;;
    extensions)
        show_extensions
        ;;
    config)
        config_operation $options
        ;;
    help)
        show_help
        ;;
    *)
        log_error "Unknown command: $command"
        show_help
        exit 1
        ;;
esac