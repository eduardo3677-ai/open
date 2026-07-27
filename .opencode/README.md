# OpenCode Configuration Documentation

## Overview
This directory contains the complete OpenCode configuration with enhanced features, agents, skills, and utilities.

## Configured Features

### 🛠️ Skills
- **code-review**: Automated code quality analysis and best practices
- **debugging**: Systematic debugging and troubleshooting
- **refactoring**: Code improvement and restructuring
- **testing**: Test writing and quality assurance

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

### Using Skills
Skills are automatically available and will be loaded when appropriate for the task.

## File Structure
```
.opencode/
├── skills/                 # Agent skills
│   ├── code-review/
│   ├── debugging/
│   ├── refactoring/
│   └── testing/
```

## Environment Variables Required
- `DASHSCOPE_API_KEY`: Azure API access

## Notes
- Configuration loaded at startup - restart needed for changes
- Skills follow naming convention: lowercase-hyphen-separated