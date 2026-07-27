#!/usr/bin/env node

/**
 * OpenCode Utility Scripts
 * Collection of helper functions for automated tasks
 */

const fs = require('fs');
const path = require('path');

/**
 * Find all files matching a pattern in a directory
 * @param {string} dir - Directory to search
 * @param {string} pattern - Glob pattern to match
 * @returns {string[]} Array of matching file paths
 */
function findFiles(dir, pattern) {
  const files = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...findFiles(fullPath, pattern));
    } else if (entry.name.match(pattern)) {
      files.push(fullPath);
    }
  }
  
  return files;
}

/**
 * Get file statistics
 * @param {string} filePath - Path to file
 * @returns {object} File statistics
 */
function getFileStats(filePath) {
  try {
    const stats = fs.statSync(filePath);
    return {
      size: stats.size,
      modified: stats.mtime,
      created: stats.birthtime,
      isFile: stats.isFile(),
      isDirectory: stats.isDirectory()
    };
  } catch (error) {
    return { error: error.message };
  }
}

/**
 * Search content in files
 * @param {string} dir - Directory to search
 * @param {string} searchTerm - Text to search for
 * @param {string[]} extensions - File extensions to search
 * @returns {object[]} Search results
 */
function searchInFiles(dir, searchTerm, extensions = ['.js', '.ts', '.json']) {
  const results = [];
  const files = findFiles(dir, /\.(js|ts|json)$/);
  
  for (const file of files) {
    const ext = path.extname(file);
    if (!extensions.includes(ext)) continue;
    
    try {
      const content = fs.readFileSync(file, 'utf-8');
      const lines = content.split('\n');
      
      lines.forEach((line, index) => {
        if (line.includes(searchTerm)) {
          results.push({
            file,
            line: index + 1,
            text: line.trim()
          });
        }
      });
    } catch (error) {
      // Skip files that can't be read
    }
  }
  
  return results;
}

/**
 * Validate JSON file
 * @param {string} filePath - Path to JSON file
 * @returns {object} Validation result
 */
function validateJSON(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const parsed = JSON.parse(content);
    return { valid: true, data: parsed };
  } catch (error) {
    return { valid: false, error: error.message };
  }
}

// CLI interface
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case 'find':
    if (args[1] && args[2]) {
      console.log(JSON.stringify(findFiles(args[1], args[2]), null, 2));
    } else {
      console.error('Usage: node utils.js find <directory> <pattern>');
    }
    break;
    
  case 'stats':
    if (args[1]) {
      console.log(JSON.stringify(getFileStats(args[1]), null, 2));
    } else {
      console.error('Usage: node utils.js stats <file>');
    }
    break;
    
  case 'search':
    if (args[1] && args[2]) {
      const exts = args[3] ? args[3].split(',') : ['.js', '.ts', '.json'];
      console.log(JSON.stringify(searchInFiles(args[1], args[2], exts), null, 2));
    } else {
      console.error('Usage: node utils.js search <directory> <searchTerm> [extensions]');
    }
    break;
    
  case 'validate':
    if (args[1]) {
      console.log(JSON.stringify(validateJSON(args[1]), null, 2));
    } else {
      console.error('Usage: node utils.js validate <jsonFile>');
    }
    break;
    
  default:
    console.log('OpenCode Utility Scripts');
    console.log('Commands: find, stats, search, validate');
    console.log('Usage: node utils.js <command> [args...]');
}