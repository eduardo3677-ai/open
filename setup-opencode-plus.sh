#!/bin/bash
# OpenCode Plus Setup Script
# This script sets up the environment and installs all dependencies

set -e

echo "🚀 Setting up OpenCode Plus environment..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Install system dependencies
log_info "Installing system dependencies..."
if command_exists apt-get; then
    sudo apt-get update
    sudo apt-get install -y ripgrep jq curl git
    log_success "System dependencies installed"
else
    log_info "Using existing package manager"
fi

# Install Node.js if not present
if ! command_exists npm; then
    log_info "Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
    log_success "Node.js installed"
fi

# Install Python if not present
if ! command_exists pip; then
    log_info "Installing Python and pip..."
    sudo apt-get install -y python3 python3-pip
    log_success "Python installed"
fi

# Build the OpenCode Plus action
log_info "Building OpenCode Plus action..."
cd .github/actions/opencode-plus
if [ -f "package.json" ]; then
    npm install
    npm run build
    npm run package
    log_success "OpenCode Plus action built successfully"
else
    log_info "No package.json found for action build"
fi
cd -

# Install MCP servers from configuration
log_info "Configuring MCP servers..."
if [ -f "opencode-plus.json" ]; then
    # Extract MCP servers configuration
    mcp_servers=$(jq -c '.mcpServers[]? | select(.enabled == true)' opencode-plus.json)
    
    if [ -n "$mcp_servers" ]; then
        echo "$mcp_servers" | while read -r server; do
            name=$(echo "$server" | jq -r '.name')
            install_cmd=$(echo "$server" | jq -r '.install // empty')
            
            log_info "Installing MCP server: $name"
            if [ -n "$install_cmd" ]; then
                eval "$install_cmd" || log_error "Failed to install $name"
                log_success "MCP server $name installed"
            fi
        done
    else
        log_info "No MCP servers configured or enabled"
    fi
fi

# Install ASP servers from configuration
log_info "Configuring ASP servers..."
if [ -f "opencode-plus.json" ]; then
    asp_servers=$(jq -c '.aspServers[]? | select(.enabled == true)' opencode-plus.json)
    
    if [ -n "$asp_servers" ]; then
        echo "$asp_servers" | while read -r server; do
            name=$(echo "$server" | jq -r '.name')
            install_cmd=$(echo "$server" | jq -r '.install // empty')
            
            log_info "Installing ASP server: $name"
            if [ -n "$install_cmd" ]; then
                eval "$install_cmd" || log_error "Failed to install $name"
                log_success "ASP server $name installed"
            fi
        done
    else
        log_info "No ASP servers configured or enabled"
    fi
fi

# Install plugins from configuration
log_info "Configuring plugins..."
if [ -f "opencode-plus.json" ]; then
    plugins=$(jq -c '.plugins[]? | select(.enabled == true)' opencode-plus.json)
    
    if [ -n "$plugins" ]; then
        echo "$plugins" | while read -r plugin; do
            name=$(echo "$plugin" | jq -r '.name')
            install_cmd=$(echo "$plugin" | jq -r '.install // empty')
            
            log_info "Installing plugin: $name"
            if [ -n "$install_cmd" ]; then
                eval "$install_cmd" || log_error "Failed to install $name"
                log_success "Plugin $name installed"
            fi
        done
    else
        log_info "No plugins configured or enabled"
    fi
fi

# Verify installations
log_info "Verifying installations..."

if command_exists rg; then
    log_success "ripgrep installed (version: $(rg --version))"
else
    log_error "ripgrep not installed"
fi

if command_exists git; then
    log_success "git installed (version: $(git --version))"
else
    log_error "git not installed"
fi

# Create .opencode directories structure if they don't exist
log_info "Creating .opencode directory structure..."
mkdir -p .opencode/skills
mkdir -p .opencode/plugins
mkdir -p .opencode/mcp-servers  
mkdir -p .opencode/asp-servers
mkdir -p .opencode/agents
log_success "Directory structure created"

echo ""
log_success "🎉 OpenCode Plus setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Configure your opencode-plus.json file with your preferred settings"
echo "2. Test the action by triggering it via GitHub comment"
echo "3. Monitor logs for detailed operation information"
echo ""