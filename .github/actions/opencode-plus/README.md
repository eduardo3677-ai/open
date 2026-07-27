# OpenCode Plus - Enhanced GitHub Action

An advanced version of OpenCode GitHub Action with terminal integration, MCP/ASP servers, plugins system, enhanced logging, and automatic compression.

## Features

✅ **Terminal Integration** - Real terminal access with safety controls  
✅ **MCP Servers** - Model Context Protocol server support  
✅ **ASP Servers** - Application Service Provider server support  
✅ **Plugins System** - Extensible plugin architecture  
✅ **Enhanced Logging** - Detailed reasoning, commands, diffs, and metrics  
✅ **Auto Compression** - Token limit detection and conversation cleanup  
✅ **ripgrep Integration** - Fast file searching built-in  
✅ **Skills & Agents** - Pre-built specialist capabilities

## Configuration

The action uses `opencode-plus.json` configuration file with the following structure:

### Core Settings
- `model`: Primary model to use
- `shell`: Shell environment for terminal commands
- `logLevel`: Logging verbosity (WARN, INFO, DEBUG)
- `compaction`: Auto-compression settings

### Extensions
- `mcpServers`: MCP server configurations
- `aspServers`: ASP server configurations  
- `plugins`: Extension plugins
- `skills`: Specialized skill modules
- `formatters`: Code formatting tools

### Enhanced Features
- `terminal`: Terminal integration settings
- `enhanced_logging`: Detailed logging configuration

## Usage

The action is configured in `.github/workflows/opencode.yml`:

```yaml
- name: Run OpenCode Plus
  uses: ./.github/actions/opencode-plus
  env:
    DASHSCOPE_API_KEY: ${{ secrets.DASHSCOPE_API_KEY }}
    GITHUB_TOKEN: ${{ secrets.PAT_TOKEN }}
    PAT_TOKEN: ${{ secrets.PAT_TOKEN }}
  with:
    model: azure/zai-org--glm-47-fp8
    share: true
    use_github_token: true
    config_path: opencode-plus.json
    install_mcp_servers: true
    install_asp_servers: true
    install_plugins: true
    max_tokens: 80000
```

## Architecture

1. **Configuration Phase** - Loads and validates opencode-plus.json
2. **Setup Phase** - Installs dependencies (ripgrep, tools)
3. **Installation Phase** - Installs MCP/ASP servers and plugins
4. **Execution Phase** - Runs OpenCode with enhanced features
5. **Monitoring Phase** - Handles auto-compression when needed

## Enhanced Logging

The action provides detailed logging output:
- Model reasoning chains
- Command executions and outputs
- File operation diffs
- Token usage tracking
- Performance metrics

## Installation

Build the action:
```bash
cd .github/actions/opencode-plus
npm install
npm run build
npm run package
```

## License

Same as parent OpenCode project