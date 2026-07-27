import * as core from '@actions/core';
import * as github from '@actions/github';
import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

interface OpenCodeConfig {
  model?: string;
  shell?: string;
  logLevel?: string;
  share?: string;
  compaction?: {
    auto?: boolean;
    prune?: boolean;
    tail_turns?: number;
    max_tokens?: number;
  };
  provider?: Record<string, any>;
  mcpServers?: Record<string, any>[];
  aspServers?: Record<string, any>[];
  plugins?: Record<string, any>[];
  skills?: Record<string, any>[];
  agents?: Record<string, any>[];
  formatters?: Record<string, any>[];
}

class OpenCodePlusAction {
  private config: OpenCodeConfig = {};
  private configPath: string;
  private workspacePath: string;

  constructor() {
    this.workspacePath = process.env.GITHUB_WORKSPACE || '/home/runner/work/open/open';
    this.configPath = path.join(this.workspacePath, core.getInput('config_path'));
  }

  async run(): Promise<void> {
    try {
      this.logInfo('Starting OpenCode Plus Action');
      
      // Load and validate configuration
      await this.loadConfiguration();
      
      // Enhanced logging setup
      this.setupEnhancedLogging();
      
      // Pre-installation steps
      await this.preInstallSetup();
      
      // Install MCP servers if configured
      if (core.getBooleanInput('install_mcp_servers')) {
        await this.installMCPServers();
      }
      
      // Install ASP servers if configured
      if (core.getBooleanInput('install_asp_servers')) {
        await this.installASPServers();
      }
      
      // Install plugins if configured
      if (core.getBooleanInput('install_plugins')) {
        await this.installPlugins();
      }
      
      // Install skills if configured
      await this.installSkills();
      
      // Install formatters if configured
      await this.installFormatters();
      
      // Configure and run OpenCode
      await this.runOpenCode();
      
    } catch (error) {
      this.logError(`Action failed: ${error}`);
      throw error;
    }
  }

  private async loadConfiguration(): Promise<void> {
    this.logInfo('Loading OpenCode configuration');
    
    if (!fs.existsSync(this.configPath)) {
      this.logWarning(`Config file not found at ${this.configPath}, using defaults`);
      return;
    }
    
    const configContent = fs.readFileSync(this.configPath, 'utf-8');
    this.config = JSON.parse(configContent);
    
    // Validate and merge with action inputs
    const inputModel = core.getInput('model');
    if (inputModel) {
      this.config.model = inputModel;
    }
    
    this.logInfo('Configuration loaded successfully');
    this.logInfo(`Model: ${this.config.model || 'default'}`);
    this.logInfo(`Shell: ${this.config.shell || '/bin/bash'}`);
    this.logInfo(`Log Level: ${this.config.logLevel || 'INFO'}`);
  }

  private setupEnhancedLogging(): void {
    this.logInfo('Setting up enhanced logging');
    
    // Set log level from config
    const logLevel = this.config.logLevel || 'INFO';
    core.setOutput('log_level', logLevel);
    
    // Configure environment variables for enhanced logging
    process.env.OPENCODE_ENHANCED_LOGGING = 'true';
    process.env.OPENCODE_SHOW_REASONING = 'true';
    process.env.OPENCODE_SHOW_COMMANDS = 'true';
    process.env.OPENCODE_SHOW_DIFFS = 'true';
    process.env.OPENCODE_LOG_LEVEL = logLevel;
    
    this.logInfo('Enhanced logging configured');
  }

  private async preInstallSetup(): Promise<void> {
    this.logInfo('Running pre-installation setup');
    
    // Install ripgrep if not available
    try {
      execSync('rg --version', { stdio: 'pipe' });
      this.logInfo('ripgrep already installed');
    } catch {
      this.logInfo('Installing ripgrep');
      execSync('sudo apt-get update && sudo apt-get install -y ripgrep', { 
        stdio: 'inherit',
        cwd: this.workspacePath
      });
      this.logInfo('ripgrep installed successfully');
    }
    
    // Set up shell from config
    const shell = this.config.shell || '/bin/bash';
    process.env.SHELL = shell;
    this.logInfo(`Shell configured: ${shell}`);
  }

  private async installMCPServers(): Promise<void> {
    const servers = this.config.mcpServers || [];
    
    if (servers.length === 0) {
      this.logInfo('No MCP servers configured');
      return;
    }
    
    this.logInfo(`Installing ${servers.length} MCP servers`);
    
    for (const server of servers) {
      try {
        this.logInfo(`Installing MCP server: ${server.name || 'unnamed'}`);
        
        if (server.install) {
          execSync(server.install, { 
            stdio: 'inherit',
            cwd: this.workspacePath,
            env: { ...process.env, ...server.env }
          });
        }
        
        this.logInfo(`MCP server ${server.name || 'unnamed'} installed successfully`);
      } catch (error) {
        this.logError(`Failed to install MCP server ${server.name || 'unnamed'}: ${error}`);
        throw error;
      }
    }
  }

  private async installASPServers(): Promise<void> {
    const servers = this.config.aspServers || [];
    
    if (servers.length === 0) {
      this.logInfo('No ASP servers configured');
      return;
    }
    
    this.logInfo(`Installing ${servers.length} ASP servers`);
    
    for (const server of servers) {
      try {
        this.logInfo(`Installing ASP server: ${server.name || 'unnamed'}`);
        
        if (server.install) {
          execSync(server.install, { 
            stdio: 'inherit',
            cwd: this.workspacePath,
            env: { ...process.env, ...server.env }
          });
        }
        
        this.logInfo(`ASP server ${server.name || 'unnamed'} installed successfully`);
      } catch (error) {
        this.logError(`Failed to install ASP server ${server.name || 'unnamed'}: ${error}`);
        throw error;
      }
    }
  }

  private async installPlugins(): Promise<void> {
    const plugins = this.config.plugins || [];
    
    if (plugins.length === 0) {
      this.logInfo('No plugins configured');
      return;
    }
    
    this.logInfo(`Installing ${plugins.length} plugins`);
    
    for (const plugin of plugins) {
      try {
        this.logInfo(`Installing plugin: ${plugin.name || 'unnamed'}`);
        
        if (plugin.install) {
          execSync(plugin.install, { 
            stdio: 'inherit',
            cwd: this.workspacePath,
            env: { ...process.env, ...plugin.env }
          });
        }
        
        this.logInfo(`Plugin ${plugin.name || 'unnamed'} installed successfully`);
      } catch (error) {
        this.logError(`Failed to install plugin ${plugin.name || 'unnamed'}: ${error}`);
        throw error;
      }
    }
  }

  private async installSkills(): Promise<void> {
    const skills = this.config.skills || [];
    
    if (skills.length === 0) {
      this.logInfo('No skills configured');
      return;
    }
    
    this.logInfo(`Installing ${skills.length} skills`);
    
    for (const skill of skills) {
      try {
        this.logInfo(`Installing skill: ${skill.name || 'unnamed'}`);
        
        if (skill.install) {
          execSync(skill.install, { 
            stdio: 'inherit',
            cwd: this.workspacePath,
            env: { ...process.env, ...skill.env }
          });
        }
        
        this.logInfo(`Skill ${skill.name || 'unnamed'} installed successfully`);
      } catch (error) {
        this.logError(`Failed to install skill ${skill.name || 'unnamed'}: ${error}`);
        throw error;
      }
    }
  }

  private async installFormatters(): Promise<void> {
    const formatters = this.config.formatters || [];
    
    if (formatters.length === 0) {
      this.logInfo('No formatters configured');
      return;
    }
    
    this.logInfo(`Installing ${formatters.length} formatters`);
    
    for (const formatter of formatters) {
      try {
        this.logInfo(`Installing formatter: ${formatter.name || 'unnamed'}`);
        
        if (formatter.install) {
          execSync(formatter.install, { 
            stdio: 'inherit',
            cwd: this.workspacePath,
            env: { ...process.env, ...formatter.env }
          });
        }
        
        this.logInfo(`Formatter ${formatter.name || 'unnamed'} installed successfully`);
      } catch (error) {
        this.logError(`Failed to install formatter ${formatter.name || 'unnamed'}: ${error}`);
        throw error;
      }
    }
  }

  private async runOpenCode(): Promise<void> {
    const model = this.config.model || core.getInput('model');
    const share = core.getInput('share');
    const useGHToken = core.getBooleanInput('use_github_token');
    const maxTokens = parseInt(core.getInput('max_tokens'));
    
    this.logInfo('Configuring OpenCode execution');
    this.logInfo(`Model: ${model}`);
    this.logInfo(`Share: ${share}`);
    this.logInfo(`Use GitHub Token: ${useGHToken}`);
    this.logInfo(`Max Tokens: ${maxTokens}`);
    
    // Configure automatic compression
    if (this.config.compaction?.auto) {
      process.env.OPENCODE_AUTO_COMPRESSION = 'true';
      process.env.OPENCODE_MAX_TOKENS = maxTokens.toString();
      process.env.OPENCODE_COMPACT_PRUNE = this.config.compaction.prune ? 'true' : 'false';
      process.env.OPENCODE_COMPACT_TAIL_TURNS = this.config.compaction.tail_turns?.toString() || '2';
      this.logInfo('Automatic compression configured');
    }
    
    // Set up environment variables
    const openCodeEnv = {
      ...process.env,
      DASHSCOPE_API_KEY: process.env.DASHSCOPE_API_KEY || '',
      GITHUB_TOKEN: process.env.PAT_TOKEN || process.env.GITHUB_TOKEN || '',
      OPENCODE_PLUS_CONFIG: JSON.stringify(this.config),
      OPENCODE_TERMINAL_INTEGRATION: 'true',
      OPENCODE_MCP_ENABLED: 'true',
      OPENCODE_ASP_ENABLED: 'true',
      OPENCODE_PLUGINS_ENABLED: 'true',
    };
    
    this.logInfo('Starting OpenCode with enhanced features');
    this.logInfo('Terminal integration: ENABLED');
    this.logInfo('MCP servers: ENABLED');
    this.logInfo('ASP servers: ENABLED');
    this.logInfo('Plugins: ENABLED');
    
    // Execute OpenCode using the standard action but with enhanced environment
    const opencodeCommand = [
      'docker run --rm',
      `-v ${this.workspacePath}:/workspace`,
      `-e DASHSCOPE_API_KEY=\${DASHSCOPE_API_KEY}`,
      `-e GITHUB_TOKEN=\${GITHUB_TOKEN}`,
      `-e OPENCODE_PLUS_CONFIG='\${OPENCODE_PLUS_CONFIG}'`,
      anomalyco/opencode/github:latest
    ].join(' ');
    
    try {
      execSync(opencodeCommand, {
        stdio: 'inherit',
        cwd: this.workspacePath,
        env: openCodeEnv
      });
      
      this.logInfo('OpenCode completed successfully');
    } catch (error) {
      this.logError(`OpenCode execution failed: ${error}`);
      throw error;
    }
  }

  private logInfo(message: string): void {
    core.info(`[OpenCode Plus] ${message}`);
    console.log(`ℹ️ [OpenCode Plus] ${message}`);
  }

  private logWarning(message: string): void {
    core.warning(`[OpenCode Plus] ${message}`);
    console.log(`⚠️ [OpenCode Plus] ${message}`);
  }

  private logError(message: string): void {
    core.error(`[OpenCode Plus] ${message}`);
    console.error(`❌ [OpenCode Plus] ${message}`);
  }
}

// Run the action
async function main(): Promise<void> {
  const action = new OpenCodePlusAction();
  await action.run();
}

main().catch(error => {
  core.setFailed(error.message);
  process.exit(1);
});