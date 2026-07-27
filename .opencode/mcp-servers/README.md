# MCP Servers Configuration for OpenCode Plus

This directory contains Model Context Protocol (MCP) server configurations for OpenCode Plus.

## Available Servers

### Filesystem Server
- **Name**: filesystem  
- **Purpose**: File system access and operations
- **Installation**: `npm install -g @modelcontextprotocol/server-filesystem`
- **Config**: Requires `MCP_SERVER_FILESYSTEM_PATH` environment variable

### GitHub Server
- **Name**: github
- **Purpose**: GitHub API integration  
- **Installation**: `npm install -g @modelcontextprotocol/server-github`
- **Config**: Requires `GITHUB_TOKEN` environment variable

### SQLite Server
- **Name**: sqlite
- **Purpose**: SQLite database operations
- **Installation**: `npm install -g @modelcontextprotocol/server-sqlite`
- **Config**: Database path configuration required

## Adding New MCP Servers

1. Create a server configuration file:
```json
{
  "name": "your-server",
  "enabled": true,
  "install": "npm install -g @modelcontextprotocol/server-your-server",
  "env": {
    "YOUR_SERVER_CONFIG": "value"
  }
}
```

2. Add to `opencode-plus.json` under `mcpServers` array

3. Restart the GitHub Action to install and configure

## MCP Protocol Support

OpenCode Plus supports these MCP capabilities:
- Tool invocation
- Resource access
- Prompt templates
- Sampling methods
- Authentication flows

## Troubleshooting

### Server Not Starting
- Check installation logs in GitHub Actions output
- Verify environment variables are set correctly
- Test server locally before deployment

### Authentication Issues  
- Verify tokens have required permissions
- Check token expiration dates
- Ensure API endpoints are accessible