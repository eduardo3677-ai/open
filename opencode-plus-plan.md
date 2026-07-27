# OpenCode Plus - Master Implementation Plan

## Overview
This plan extends OpenCode with comprehensive enhancements including artifact storage, terminal capabilities, server integration, improved message formatting, and automated conversation management.

## Architecture Multipliers

### 1. Configuration Runtime Engine
- **opencode.json** loading with validation
- Dynamic plugin/skill/agent registration
- ASP/MCP server bootstrap
- Auto-install on GitHub action startup
- Local development compatibility

### 2. Enhanced Message Rendering
- Model reasoning traces in logs
- Tool execution summaries (bash, edit, grep)
- Differential outputs (read/new/changes)
- Timestamps, session IDs, severity indicators
- Formatted markdown messages to stdout & logs

### 3. File System Acceleration
- Ripgrep integration for fast content search
- Optimized file pattern matching
- Streamlined diff creation
- LFS-aware source retrieval

### 4. Server Integration Matrix
- **ASP Servers**: Azure service providers
- **MCP Servers**: Model Context Protocol endpoints
- **Plugins**: Extensible functionality modules
- **Skills**: Domain-specific agents
- **Formatters**: Output processors

### 5. Conversation Gestalt
- Token limit detection
- Automated compression/decompression
- Pruning triggers on limits
- Context summarization

## Implementation Steps

### Phase 1: Foundation Layer
- [ ] Parse and validate `opencode.json`
- [ ] Create schema and loader utilities
- [ ] Add runtime config service
- [ ] Set up boot manager for extensions

### Phase 2: Capability Incorporation
- [ ] Install package dependencies
- [ ] Boot ASP/MCP servers from config
- [ ] Load plugins and skills
- [ ] Register formatter pipelines

### Phase 3: Terminal & Tools Expansion
- [ ] Integrate real PTY terminal
- [ ] Add bash shell tool hooks
- [ ] Integrate ripgrep into file operations
- [ ] Hook diff generation for changes

### Phase 4: Instrumentation & Logging
- [ ] Format reasoning messages with metadata
- [ ] Show tool invocations (command, args, output)
- [ ] Transform logs for runner consumption
- [ ] Add diff rendering for edits

### Phase 5: Conversation Management
- [ ] Token limit tracking
- [ ] Compression heuristics
- [ ] Auto-compaction trigger
- [ ] Summarization pipeline

### Phase 6: GitHub Action Integration
- [ ] Action-level config preloading
- [ ] Install servers prior to model startup
- [ ] Apply dynamic capabilities
- [ ] Connect session to collection service

### Phase 7: Local Development Support
- [ ] Preserve easy startup flow
- [ ] shell-compatibility hooks
- [ ] Quick config validation
- [ ] Developer diagnostics

## Critical Files to Modify/Extend

### GitHub Action
- `github/index.ts` - Configuration loading, session boots, message enhancement
- `github/action.yml` - Input expansion (confidence threshold, compression level)

### CLI
- `packages/cli/src/commands/run.ts` - Argument parsing & runtime config
- `packages/opencode/src/` - Core logic for session and compose

### Core
- `packages/core/src/` - Schema validation, config loader, collector extension
- `packages/http-recorder/src/` - Replay and diff utilities

### Utilities
- New `packages/opencode-plus/src/` - Extended runtime engine with plugins/skills/asp/mcp
- `scripts/install_plus.sh` - One-click setup script

## Configuration Format

```json
{
  "$schema": "https://opencode.ai/config-plus.json",
  "model": "azure/zai-org--glm-47-fp8",
  "small_model": "azure/zai-org--glm-47-fp8",
  "shell": "/bin/bash",
  "logLevel": "INFO",
  "compaction": {
    "auto": true,
    "prune": true,
    "tailTurns": 2
  },
  "extensions": {
    "plugins": ["opencode-wakatime", "opencode-notifier"],
    "skills": ["code-review", "debugging", "refactoring", "testing"],
    "agents": ["expert", "reviewer"],
    "asp_servers": [
      {
        "id": "azure-main",
        "endpoint": "https://asp.example.com",
        "auth": "env:AZURE_KEY"
      }
    ],
    "mcp_servers": [
      {
        "id": "github",
        "type": "github",
        "config": {
          "token": "env:GITHUB_TOKEN"
        }
      }
    ]
  },
  "logging": {
    "show_reasoning": true,
    "show_tool_calls": true,
    "show_diffs": true,
    "format": "markdown"
  },
  "tools": {
    "use_ripgrep": true,
    "term_pty": true
  },
  "permission": {
    "edit": "ask",
    "bash": {"git *": "allow", "*": "ask"},
    "external_directory": {"~/projects/**": "allow", "*": "deny"}
  }
}
```

## Installation Process

### GitHub Action
1. Clone repository with preset `opencode.json`
2. Install dependencies via Bun
3. Parse `opencode.json`, validate, and load
4. Boot ASP/MCP servers
5. Install plugins and register formatters
6. Start session with loaded configuration
7. Run model with extensions active

### Local Development
```bash
# Quick start
bun install
./scripts/install_plus.sh
opencode run

# Validate configuration
opencode validate-config

# Show loaded extensions
opencode extensions list
```

## Foreground In-Progress: Conversation Compression Logic

When token usage approaches the context limit:
1. Capture recent user prompts and model responses
2. Generate summary using small model
3. Remove older turns while preserving system prompts
4. Continue session with reduced context
5. Log compression event with metadata

## Testing Strategy

- Unit tests for config validation
- Integration tests for plugin loading
- End-to-end GitHub action workflow
- Local developer manual validation
- Performance benchmarks for ripgrep integration
- Token compression boundary testing

## Rollout

1. Feature flags for each phase
2. Graceful degradation if extensions fail
3. Local mode toggles for extensive development
4. Detailed error messages with context
5. Rollback script for configuration issues
