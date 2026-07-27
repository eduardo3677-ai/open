# OpenCode Plus - Enhanced GitHub Action

An advanced version of OpenCode GitHub Action with comprehensive terminal integration, MCP/ASP servers, plugin system, enhanced logging, and automatic conversation compression.

## 🚀 Key Features

- **🖥️ Terminal Integration**: Real terminal access with safety controls and timeout management
- **🔌 MCP Servers**: Model Context Protocol server support for extended capabilities  
- **⚡ ASP Servers**: Application Service Provider server integration
- **🧩 Plugin System**: Extensible architecture for custom tools and formatters
- **📊 Enhanced Logging**: Detailed reasoning chains, command outputs, diffs, and performance metrics
- **🤖 Auto Compression**: Automatic token limit detection and intelligent conversation cleanup
- **🔍 ripgrep Integration**: Built-in fast file searching
- **🎯 Skills & Agents**: Pre-built specialist capabilities for code review, debugging, testing

## 📋 Quick Start

1. **Configure Settings**: Edit `opencode-plus.json` with your preferences
2. **Install Dependencies**: Run `./setup-opencode-plus.sh` to set up environment  
3. **Trigger Action**: Comment `/oc` on any issue or PR to start

## 🛠️ The Action

OpenCode Plus uses a custom GitHub Action located at `.github/actions/opencode-plus/`. This action:

1. **Configuration Phase**: Loads and validates `opencode-plus.json`
2. **Setup Phase**: Installs dependencies (ripgrep, tools)
3. **Installation Phase**: Installs MCP/ASP servers and plugins
4. **Execution Phase**: Runs OpenCode with enhanced features
5. **Monitoring Phase**: Handles auto-compression when token limits reached

## 📁 File Structure

```
.github/
  workflows/
    opencode.yml          # Main workflow file
  actions/
    opencode-plus/        # Custom action
      src/
        index.ts         # Main action logic
      package.json
      tsconfig.json
      action.yml
.opencode/
  skills/                # Specialist capabilities
  plugins/              # Extensible tools
  mcp-servers/          # MCP server configs
  agents/               # Agent configurations
opencode-plus.json     # Main configuration
setup-opencode-plus.sh # Setup script
```

## 🔧 Configuration File

`opencode-plus.json` contains all configuration:

### Core Settings
- `model`: Primary model to use
- `shell`: Terminal environment  
- `logLevel`: Logging verbosity
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

## 💻 Usage

To invoke OpenCode Plus, add a comment on any issue or PR containing `/oc` or `/opencode`.

```
/oc Please review this code for security vulnerabilities
```

## 🔌 MCP Servers

OpenCode Plus supports these MCP servers out of the box:

- **Filesystem**: File operations and management
- **GitHub**: GitHub API integration
- **SQLite**: Database operations

Add more in `opencode-plus.json` under `mcpServers`.

## ⚡ ASP Servers  

Supported ASP servers:

- **Code Analysis**: Dynamic code analysis
- **Security Scanner**: Automated security scanning

Configure in `opencode-plus.json` under `aspServers`.

## 🧩 Plugin System

Built-in plugins include:

- **ESLint**: JavaScript linting  
- **Prettier**: Code formatting
- **File Operations**: Enhanced file management

Create custom plugins using the `.opencode/plugins/` directory.

## 📊 Enhanced Logging

The action provides detailed logs:

- Model reasoning chains
- Command executions with outputs
- File operation diffs  
- Token usage tracking
- Performance metrics

Configure in `enhanced_logging` section of configuration.

## 🤖 Auto Compression

When token limits are approached, OpenCode Plus automatically:

- Detects token usage approaching limit
- Identifies conversation points to compress  
- Preserves recent context and key decisions
- Maintains conversation continuity

Configure in `compaction` section.

## 🔍 Skills

Pre-built specialist skills:

- **Code Review**: Quality and standards assessment
- **Debugging**: Systematic troubleshooting  
- **Refactoring**: Code structure improvements
- **Testing**: Test coverage and quality

Located in `.opencode/skills/`.

## 🛡️ Security

- Terminal commands have timeout limits
- Dangerous operations require confirmation
- File operations are tracked and logged
- Token-based authentication

## 📈 Performance

- Fast file operations using ripgrep
- Parallel server installations
- Efficient memory management  
- Optimized logging pipeline

## 🔑 Required Secrets

Configure these repository secrets:

- `DASHSCOPE_API_KEY`: Azure/OpenAI API key
- `PAT_TOKEN`: GitHub personal access token (for operations)

## 🚀 Production Deployment

1. `.github/workflows/opencode.yml`: Already configured to use local action
2. `.github/actions/opencode-plus/`: Custom action files
3. `opencode-plus.json`: Production configuration
4. `setup-opencode-plus.sh`: Environment setup if needed

## 📝 Development

Build the action:
```bash
cd .github/actions/opencode-plus
npm install
npm run build  
npm run package
```

Test locally:
```bash
npm run test
```

## 🤝 Contributing

Add new features by:
1. Editing `.github/actions/opencode-plus/src/index.ts`
2. Updating `opencode-plus.json` configuration
3. Testing with GitHub workflows

## 📄 License

Same as parent OpenCode project

## 🆘 Troubleshooting

### Action Not Starting
- Check workflow permissions in repository settings
- Verify secrets are correctly configured
- Review GitHub Actions logs

### Servers Not Installing  
- Check network connectivity
- Verify server URLs are accessible
- Review installation logs

### Memory Issues
- Reduce concurrent operations in config
- Lower max tokens threshold
- Enable more aggressive compaction

## 🔗 Resources

- [OpenCode Documentation](https://opencode.ai)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)