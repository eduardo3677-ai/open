#!/usr/bin/env node

/**
 * Code Analysis Script for OpenCode
 * Analyzes code quality, complexity, and patterns
 */

const fs = require('fs');
const path = require('path');

/**
 * Calculate cyclomatic complexity
 * @param {string} code - Code to analyze
 * @returns {number} Complexity score
 */
function calculateComplexity(code) {
  let complexity = 1;
  const patterns = [
    /\bif\b/g,
    /\belse\b/g,
    /\bfor\b/g,
    /\bwhile\b/g,
    /\bswitch\b/g,
    /\bcase\b/g,
    /\bcatch\b/g,
    /\b&&\b/g,
    /\b\|\|\b/g,
    /\?/g
  ];
  
  patterns.forEach(pattern => {
    const matches = code.match(pattern);
    if (matches) complexity += matches.length;
  });
  
  return complexity;
}

/**
 * Analyze a single file
 * @param {string} filePath - Path to file
 * @returns {object} Analysis results
 */
function analyzeFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const ext = path.extname(filePath);
    const stats = fs.statSync(filePath);
    
    const analysis = {
      file: filePath,
      size: stats.size,
      lines: content.split('\n').length,
      complexity: 0,
      issues: []
    };
    
    // Language-specific analysis
    if (['.js', '.ts', '.jsx', '.tsx'].includes(ext)) {
      analysis.complexity = calculateComplexity(content);
      analysis.language = path.basename(ext).replace('.', '');
      
      // Check for common issues
      if (content.includes('console.log')) {
        analysis.issues.push('Contains console.log statements');
      }
      if (content.includes('TODO') || content.includes('FIXME')) {
        analysis.issues.push('Contains TODO/FIXME comments');
      }
      if (content.includes('var ')) {
        analysis.issues.push('Uses var instead of const/let');
      }
    }
    
    return analysis;
  } catch (error) {
    return { file: filePath, error: error.message };
  }
}

/**
 * Analyze directory
 * @param {string} dir - Directory to analyze
 * @param {string[]} extensions - File extensions to analyze
 * @returns {object[]} Array of file analyses
 */
function analyzeDirectory(dir, extensions = ['.js', '.ts', '.jsx', '.tsx']) {
  const analyses = [];
  
  function walkDirectory(currentDir) {
    const entries = fs.readdirSync(currentDir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);
      
      if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== 'node_modules') {
        walkDirectory(fullPath);
      } else if (entry.isFile()) {
        const ext = path.extname(fullPath);
        if (extensions.includes(ext)) {
          const analysis = analyzeFile(fullPath);
          if (!analysis.error) {
            analyses.push(analysis);
          }
        }
      }
    }
  }
  
  walkDirectory(dir);
  return analyses;
}

/**
 * Generate summary report
 * @param {object[]} analyses - Array of file analyses
 * @returns {object} Summary statistics
 */
function generateSummary(analyses) {
  const summary = {
    totalFiles: analyses.length,
    totalLines: analyses.reduce((sum, a) => sum + a.lines, 0),
    totalComplexity: analyses.reduce((sum, a) => sum + a.complexity, 0),
    averageComplexity: 0,
    highComplexityFiles: [],
    filesWithIssues: []
  };
  
  if (analyses.length > 0) {
    summary.averageComplexity = summary.totalComplexity / analyses.length;
  }
  
  analyses.forEach(analysis => {
    if (analysis.complexity > 10) {
      summary.highComplexityFiles.push({
        file: analysis.file,
        complexity: analysis.complexity
      });
    }
    if (analysis.issues.length > 0) {
      summary.filesWithIssues.push({
        file: analysis.file,
        issues: analysis.issues
      });
    }
  });
  
  return summary;
}

// CLI interface
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case 'file':
    if (args[1]) {
      const analysis = analyzeFile(args[1]);
      console.log(JSON.stringify(analysis, null, 2));
    } else {
      console.error('Usage: node analysis.js file <filePath>');
    }
    break;
    
  case 'directory':
    const dir = args[1] || '.';
    const exts = args[2] ? args[2].split(',') : ['.js', '.ts', '.jsx', '.tsx'];
    const analyses = analyzeDirectory(dir, exts);
    console.log(JSON.stringify(analyses, null, 2));
    break;
    
  case 'summary':
    const summaryDir = args[1] || '.';
    const summaryExts = args[2] ? args[2].split(',') : ['.js', '.ts', '.jsx', '.tsx'];
    const summaryAnalyses = analyzeDirectory(summaryDir, summaryExts);
    const summary = generateSummary(summaryAnalyses);
    console.log(JSON.stringify(summary, null, 2));
    break;
    
  default:
    console.log('OpenCode Analysis Script');
    console.log('Commands: file, directory, summary');
    console.log('Usage: node analysis.js <command> [args...]');
}