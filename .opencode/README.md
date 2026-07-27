# OpenCode Configuration Documentation

## Overview
This directory contains the complete OpenCode configuration with enhanced features, agents, skills, and utilities.

## Configured Features

### 🤖 Agents
- **expert**: Primary agent for complex coding tasks with deep reasoning
- **reviewer**: Specialized code review agent for quality assurance

### 🛠️ Skills
- **code-review**: Automated code quality analysis and best practices
- **debugging**: Systematic debugging and troubleshooting
- **refactoring**: Code improvement and restructuring
- **testing**: Test writing and quality assurance

### 🔌 Plugins
- **opencode-wakatime**: Track coding time and productivity
- **opencode-notifier**: Desktop notifications for events
- **opencode-type-inject**: Auto-inject TypeScript types

### 🌐 MCP Servers
- **GitHub**: Integration with GitHub API using workflow token
- **ASP**: Local server for Azure-specific tools

### 📜 Commands
- **review**: Automated code review
- **optimize**: Performance optimization analysis

## Utility Scripts

### backup.js
 automated backup system with:
- Create timestamped backups
- List available backups  
- Clean old backups (keep last N)

### analysis.js
Code quality analysis tools:
- Calculate cyclomatic complexity
- Identify code smells
- Generate summary reports
- Analyze files and directories

### utils.js
General utilities:
- File search with patterns
- File statistics
- Content search in files
- JSON validation

## Configuration Options

### Model Settings
- **Primary Model**: azure/zai-org--glm-47-fp8
- **Small Model**: azure/zai-org--glm-47-fp8
- **Enhanced Features**: Tool falling back, reasoning enabled
- **Parameters**: Temp 0.6, max tokens 4096

### Permissions
- **Edit**: Ask by default
- **Bash**: Git commands allowed, others ask permission
- **External Directories**: Configured for safe access

### Experimental Features
- **Primary Tools**: edit, bash
- **MCP Timeout**: 30 seconds
- **Batch Tool**: Enabled for parallel operations
- **Continue Loop**: Enabled on permission deny

## Usage

### Running Utilities
```bash
# Create backup
npm run backup create <source>

# List backups  
npm run backup list

# Analyze code
npm run analyze directory . <extensions>

# Generate summary
npm run analyze summary .
```

### Using Commands
```bash
/oc review
/oc optimize
```

### Accessing MCP Tools
- GitHub API tools automatically available
- ASP tools for Azure operations

## File Structure
```
.opencode/
├── opencode.json           # Main configuration
├── scripts/                # Utility scripts
│   ├── backup.js
│   ├── analysis.js
│   └── utils.js
├── skills/                 # Agent skills
│   ├── code-review/
│   ├── debugging/
│   ├── refactoring/
│   └── testing/
├── agents/                 # Custom agents
│   ├── expert.md
│   └── reviewer.md
└── package.json           # Scripts dependencies

## Best Practices

1. **Regular Backups**: Use backup.js before major changes
2. **Code Quality**: Run analysis.js regularly to maintain standards
3. **Reviews**: Use /oc review for PR quality checks  
4. **Testing**: Leverage testing skill for comprehensive test coverage

## Environment Variables Required
- `DASHSCOPE_API_KEY`: Azure API access
- `GITHUB_TOKEN`: GitHub API access (provided by workflow)

## Notes
- Configuration loaded at startup - restart needed for changes
- MCP servers add context overhead - use judiciously
- Skills follow naming convention: lowercase-hyphen-separated
- Agents can be customized in .opencode/agents/ directory