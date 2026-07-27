#!/usr/bin/env python3
"""
Advanced analysis of Acer executables for download functionality.
This script searches for specific patterns related to download logic.
"""

import os
import re
import json
from pathlib import Path

class AdvancedAcerAnalyzer:
    def __init__(self, base_dir="acer-analysis"):
        self.base_dir = Path(base_dir)
        self.download_patterns = [
            # URL patterns
            r'https?://[^\s<>"]+',
            r'ftps?://[^\s<>"]+',
            
            # Download-related keywords
            r'(download|update|fetch|retrieve|get|fetch)\s*url',
            r'(url|uri|path)\s*:\s*[\'"][^\'"]+[\'"]',
            r'\.exe\b.*\.(zip|rar|7z|msi|bin)\b',
            
            # Server patterns
            r'server\s*[:=]\s*[\'"][^\'"]+[\'"]',
            r'host\s*[:=]\s*[\'"][^\'"]+[\'"]',
            
            # Request patterns
            r'User-Agent.*:[^\n\r]+',
            r'Content-Type.*:[^\n\r]+',
            
            # Acer-specific
            r'(?i)acer.*server',
            r'(?i)acer.*download',
            r'(?i)acer.*update',
            r'(?i)global.*download',
            r'(?i)GDFiles',
        ]
        
        self.interesting_files = []
        self.findings = []
        
    def binary_search(self, filepath, patterns):
        """Search for binary strings in a file."""
        findings = []
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
                
            # Convert to string for regex searching
            data_str = data.decode('utf-8', errors='ignore')
            
            for pattern in patterns:
                matches = re.finditer(pattern, data_str, re.IGNORECASE)
                for match in matches:
                    context_start = max(0, match.start() - 50)
                    context_end = min(len(data_str), match.end() + 50)
                    context = data_str[context_start:context_end].strip()
                    
                    findings.append({
                        'pattern': pattern,
                        'match': match.group(),
                        'context': context
                    })
                    
        except Exception as e:
            pass
            
        return findings
    
    def analyze_binary(self, filepath):
        """Analyze a binary file for download functionality."""
        findings = self.binary_search(filepath, self.download_patterns)
        
        if findings:
            self.interesting_files.append(str(filepath))
            for finding in findings:
                finding['file'] = str(filepath)
                self.findings.append(finding)
                
        return findings
    
    def find_target_files(self):
        """Find likely target files for analysis."""
        target_files = []
        
        # Focus on main executables and DLLs
        extensions = ['.exe', '.dll']
        
        for ext in extensions:
            for filepath in self.base_dir.rglob('*' + ext):
                # Skip very small files and very large DLLs
                size = filepath.stat().st_size
                if 10000 < size < 10000000:  # 10KB to 10MB
                    target_files.append(filepath)
                    
        return target_files
    
    def search_for_post_data(self, filepath):
        """Search for POST request patterns that might contain headers."""
        post_patterns = [
            r'POST\s+[^\s]+\s+HTTP/\d\.\d',
            r'Content-Type:\s*application/[^\s]+',
            r'Content-Type:\s*multipart/form-data',
            r'Cookie:\s*[^\s\r\n=]+=[^\s\r\n;]+',
            r'Authorization:\s*[^\s\r\n]+',
            r'X-\w+:\s*[^\s\r\n]+',
        ]
        
        findings = []
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
                
            data_str = data.decode('utf-8', errors='ignore')
            
            for pattern in post_patterns:
                matches = re.finditer(pattern, data_str, re.IGNORECASE)
                for match in matches:
                    # Get more context for POST patterns
                    context_start = max(0, match.start() - 200)
                    context_end = min(len(data_str), match.end() + 200)
                    context = data_str[context_start:context_end].strip()
                    
                    findings.append({
                        'pattern': pattern,
                        'match': match.group(),
                        'context': context,
                        'type': 'post_data'
                    })
                    
        except Exception as e:
            pass
            
        return findings
    
    def search_for_factory_image_patterns(self, filepath):
        """Search for factory image download patterns."""
        factory_patterns = [
            r'(?i)factory.*image',
            r'(?i)recovery.*image',
            r'(?i)iso.*download',
            r'(?i)restore.*image',
            r'(?i)backup.*image',
            r'(?i)A315-59',
            r'(?i)ASPIRE.*A315',
        ]
        
        findings = []
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
                
            data_str = data.decode('utf-8', errors='ignore')
            
            for pattern in factory_patterns:
                matches = re.finditer(pattern, data_str)
                for match in matches:
                    context_start = max(0, match.start() - 100)
                    context_end = min(len(data_str), match.end() + 100)
                    context = data_str[context_start:context_end].strip()
                    
                    findings.append({
                        'pattern': pattern,
                        'match': match.group(),
                        'context': context,
                        'type': 'factory_pattern'
                    })
                    
        except Exception as e:
            pass
            
        return findings
    
    def comprehensive_analysis(self):
        """Perform comprehensive analysis of all files."""
        target_files = self.find_target_files()
        print(f"Analyzing {len(target_files)} target files...")
        
        results = {
            'summary': {
                'total_files_analyzed': len(target_files),
                'files_with_findings': 0,
                'total_findings': 0,
                'finding_types': {}
            },
            'findings_by_file': {},
            'post_data-findings': [],
            'factory_image_patterns': []
        }
        
        for filepath in target_files:
            print(f"Analyzing: {filepath.name}")
            
            # General download pattern analysis
            general_findings = self.analyze_binary(filepath)
            
            # POST request analysis
            post_findings = self.search_for_post_data(filepath)
            
            # Factory image pattern analysis
            factory_findings = self.search_for_factory_image_patterns(filepath)
            
            if general_findings or post_findings or factory_findings:
                results['findings_by_file'][str(filepath)] = {
                    'general_findings': general_findings,
                    'post_findings': post_findings,
                    'factory_findings': factory_findings
                }
                
                results['summary']['files_with_findings'] += 1
                results['summary']['total_findings'] += len(general_findings) + len(post_findings) + len(factory_findings)
                
                if general_findings:
                    results['summary']['finding_types']['general'] = results['summary']['finding_types'].get('general', 0) + len(general_findings)
                if post_findings:
                    results['summary']['finding_types']['post_data'] = results['summary']['finding_types'].get('post_data', 0) + len(post_findings)
                    results['post_data-findings'].extend([{'file': str(filepath), **f} for f in post_findings])
                if factory_findings:
                    results['summary']['finding_types']['factory_patterns'] = results['summary']['finding_types'].get('factory_patterns', 0) + len(factory_findings)
                    results['factory_image_patterns'].extend([{'file': str(filepath), **f} for f in factory_findings])
        
        return results
    
    def save_report(self, results, output_file="advanced_analysis_report.json"):
        """Save the analysis results."""
        try:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Advanced analysis report saved to {output_file}")
        except Exception as e:
            print(f"Error saving report: {e}")
    
    def print_summary(self, results):
        """Print a summary of findings."""
        print("\n" + "=" * 50)
        print("ADVANCED ANALYSIS SUMMARY")
        print("=" * 50)
        print(f"Files analyzed: {results['summary']['total_files_analyzed']}")
        print(f"Files with findings: {results['summary']['files_with_findings']}")
        print(f"Total findings: {results['summary']['total_findings']}")
        print(f"Finding types: {results['summary']['finding_types']}")
        
        if results['post_data-findings']:
            print(f"\nHTTP POST/Request findings: {len(results['post_data-findings'])}")
            
        if results['factory_image_patterns']:
            print(f"Factory image patterns: {len(results['factory_image_patterns'])}")
            print("\nFactory image pattern examples:")
            for finding in results['factory_image_patterns'][:5]:
                print(f"  File: {Path(finding['file']).name}")
                print(f"  Pattern: {finding['match']}")
                print()

def main():
    print("Advanced Acer Executable Analysis")
    print("=" * 50)
    
    analyzer = AdvancedAcerAnalyzer()
    
    # Perform comprehensive analysis
    results = analyzer.comprehensive_analysis()
    
    # Save report
    analyzer.save_report(results, "acer-analysis/advanced_analysis_report.json")
    
    # Print summary
    analyzer.print_summary(results)

if __name__ == "__main__":
    main()