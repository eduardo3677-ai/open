#!/usr/bin/env node

/**
 * Backup Script for OpenCode
 * Creates backups of important files and directories
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

/**
 * Create backup with timestamp
 * @param {string} source - Source path to backup
 * @param {string} backupDir - Backup directory
 */
function createBackup(source, backupDir = '.opencode/backups') {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupPath = path.join(backupDir, `${path.basename(source)}-${timestamp}`);
  
  try {
    // Create backup directory if it doesn't exist
    if (!fs.existsSync(backupDir)) {
      fs.mkdirSync(backupDir, { recursive: true });
    }
    
    // Copy files recursively
    if (fs.statSync(source).isDirectory()) {
      execSync(`cp -r "${source}" "${backupPath}"`, { stdio: 'inherit' });
    } else {
      fs.copyFileSync(source, backupPath);
    }
    
    console.log(`Backup created: ${backupPath}`);
    return backupPath;
  } catch (error) {
    console.error(`Backup failed: ${error.message}`);
    throw error;
  }
}

/**
 * List all backups
 * @param {string} backupDir - Backup directory
 */
function listBackups(backupDir = '.opencode/backups') {
  if (!fs.existsSync(backupDir)) {
    console.log('No backups found');
    return [];
  }
  
  const backups = fs.readdirSync(backupDir);
  console.log('Available backups:');
  backups.forEach(backup => {
    const fullPath = path.join(backupDir, backup);
    const stats = fs.statSync(fullPath);
    console.log(`  ${backup} (${stats.size} bytes, ${stats.mtime.toLocaleString()})`);
  });
  
  return backups;
}

/**
 * Clean old backups (keep last N)
 * @param {number} keep - Number of backups to keep
 * @param {string} backupDir - Backup directory
 */
function cleanBackups(keep = 5, backupDir = '.opencode/backups') {
  if (!fs.existsSync(backupDir)) {
    console.log('No backups to clean');
    return;
  }
  
  const backups = fs.readdirSync(backupDir)
    .map(name => ({
      name,
      path: path.join(backupDir, name),
      time: fs.statSync(path.join(backupDir, name)).mtime.getTime()
    }))
    .sort((a, b) => b.time - a.time);
  
  const toDelete = backups.slice(keep);
  
  toDelete.forEach(backup => {
    fs.rmSync(backup.path, { recursive: true, force: true });
    console.log(`Deleted old backup: ${backup.name}`);
  });
  
  console.log(`Kept ${Math.min(keep, backups.length)} most recent backups`);
}

// CLI interface
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case 'create':
    if (args[1]) {
      const backupDir = args[2] || '.opencode/backups';
      createBackup(args[1], backupDir);
    } else {
      console.error('Usage: node backup.js create <source> [backupDir]');
    }
    break;
    
  case 'list':
    const listDir = args[1] || '.opencode/backups';
    listBackups(listDir);
    break;
    
  case 'clean':
    const keepCount = parseInt(args[1]) || 5;
    const cleanDir = args[2] || '.opencode/backups';
    cleanBackups(keepCount, cleanDir);
    break;
    
  default:
    console.log('OpenCode Backup Script');
    console.log('Commands: create, list, clean');
    console.log('Usage: node backup.js <command> [args...]');
}