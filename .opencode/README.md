# OpenCode Configuration

## Configuration

### Agents
- **expert**: Primary agent for production-ready code with comprehensive testing
- **reviewer**: Subagent for code review and quality assurance

### Skills
- **code-review**: Code quality analysis and best practices
- **debugging**: Systematic debugging and troubleshooting
- **refactoring**: Code improvement and restructuring
- **testing**: Test writing and quality assurance

### Settings
- Model: azure/zai-org--glm-47-fp8
- Permissions: Edit and bash allowed
- Tools: edit, bash (primary tools enabled)

## Environment
- `DASHSCOPE_API_KEY`: Required for Azure API access

Restart opencode after configuration changes.