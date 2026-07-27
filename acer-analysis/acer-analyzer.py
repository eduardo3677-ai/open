#!/usr/bin/env python3
"""
Analyze Acer software executables for download logic and network communication patterns.
"""

import os
import sys
import re
import json
import string
from pathlib import Path
from urllib.parse import urlparse

try:
    import pefile
    from capstone import *
except ImportError as e:
    print(f"Error importing required libraries: {e}")
    sys.exit(1)

class AcerExecutableAnalyzer:
    def __init__(self, base_dir="acer-analysis"):
        self.base_dir = Path(base_dir)
        self.results = {
            "downloads": [],
            "urls": [],
            "network_patterns": [],
            "certificate_info": [],
            "suspicious_strings": []
        }
        
    def find_executables(self):
        """Find all .exe and .dll files in the analysis directory."""
        executables = []
        for ext in ['*.exe', '*.dll']:
            executables.extend(self.base_dir.rglob(ext))
        return executables
    
    def extract_strings(self, filepath, min_length=4):
        """Extract printable strings from a binary file."""
        strings = []
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
                
            # Extract ASCII strings
            current_string = ""
            for byte in data:
                if byte in range(32, 127):  # Printable ASCII
                    current_string += chr(byte)
                else:
                    if len(current_string) >= min_length:
                        strings.append(current_string)
                    current_string = ""
                    
        except Exception as e:
            print(f"Error extracting strings from {filepath}: {e}")
            
        return strings
    
    def find_urls(self, strings):
        """Find URLs in strings."""
        url_patterns = [
            r'https?://[^\s<>"]+',
            r'ftps?://[^\s<>"]+',
            r'www\.[^\s<>"]+\.[^\s<>"]+',
        ]
        
        urls = []
        for pattern in url_patterns:
            urls.extend(re.findall(pattern, ' '.join(strings), re.IGNORECASE))
            
        return list(set(urls))
    
    def analyze_pe_file(self, filepath):
        """Analyze a PE (Portable Executable) file."""
        info = {
            "file": str(filepath),
            "size": filepath.stat().st_size,
            "urls": [],
            "network_strings": [],
            "interesting_strings": []
        }
        
        try:
            # Use pefile for detailed analysis
            pe = pefile.PE(filepath)
            
            # Extract basic PE info
            if hasattr(pe, 'FILE_HEADER'):
                info["machine"] = hex(pe.FILE_HEADER.Machine)
                info["timestamp"] = pe.FILE_HEADER.TimeDateStamp
                
            if hasattr(pe, 'OPTIONAL_HEADER'):
                info["entry_point"] = hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
                info["image_base"] = hex(pe.OPTIONAL_HEADER.ImageBase)
                
            # Extract certificate information
            if hasattr(pe, 'DIRECTORY_ENTRY_SECURITY'):
                info["has_certificate"] = True
                try:
                    for security in pe.DIRECTORY_ENTRY_SECURITY:
                        # This is a simplified approach - actual cert parsing would be more complex
                        info["certificate_info"] = "Certificate present"
                except:
                    pass
            else:
                info["has_certificate"] = False
                
            pe.close()
            
        except Exception as e:
            info["pe_error"] = str(e)
        
        # Extract strings from the file
        strings = self.extract_strings(filepath)
        
        # Find URLs
        urls = self.find_urls(strings)
        info["urls"] = urls
        
        if urls:
            self.results["urls"].extend([{"file": str(filepath), "url": url} for url in urls])
        
        # Look for network-related strings
        network_keywords = [
            'download', 'http', 'https', 'ftp', 'url', 'server', 'connect',
            'request', 'response', 'get', 'post', 'proxy', 'socket',
            'acer server', 'update', 'version'
        ]
        
        network_strings = []
        for s in strings:
            s_lower = s.lower()
            for keyword in network_keywords:
                if keyword in s_lower:
                    network_strings.append(s)
                    break
                    
        info["network_strings"] = network_strings[:50]  # Limit output
        
        # Look for specific Acer-related patterns
        acer_patterns = [
            r'acer[.-_]\w+',
            r'global-download\.acer\.com',
            r'GDFiles',
            r'acerid',
            r'ASPIRE'
        ]
        
        acer_strings = []
        for pattern in acer_patterns:
            matches = re.findall(pattern, ' '.join(strings), re.IGNORECASE)
            acer_strings.extend(matches)
            
        info["acer_strings"] = list(set(acer_strings))
        
        return info
    
    def analyze_all_executables(self):
        """Analyze all executables in the directory."""
        executables = self.find_executables()
        print(f"Found {len(executables)} executables to analyze")
        
        analysis_results = []
        
        for exe in executables:
            print(f"Analyzing: {exe}")
            try:
                result = self.analyze_pe_file(exe)
                analysis_results.append(result)
            except Exception as e:
                print(f"Error analyzing {exe}: {e}")
                
        return analysis_results
    
    def generate_report(self, results):
        """Generate a comprehensive report."""
        report = {
            "summary": {
                "total_analyzed": len(results),
                "files_with_urls": sum(1 for r in results if r["urls"]),
                "unique_urls": len(set(item["url"] for item in self.results["urls"])),
            },
            "detailed_results": results,
            "all_urls": list(set(item["url"] for item in self.results["urls"])),
            "network_findings": self.results["network_patterns"]
        }
        
        return report
    
    def save_report(self, report, output_file="analysis_report.json"):
        """Save the analysis report to a JSON file."""
        try:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"Report saved to {output_file}")
        except Exception as e:
            print(f"Error saving report: {e}")

def main():
    print("Acer Software Executable Analyzer")
    print("=" * 50)
    
    analyzer = AcerExecutableAnalyzer()
    
    # Analyze all executables
    results = analyzer.analyze_all_executables()
    
    # Generate report
    report = analyzer.generate_report(results)
    
    # Save report
    analyzer.save_report(report, "acer-analysis/analysis_report.json")
    
    # Print summary
    print("\n" + "=" * 50)
    print("ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"Total files analyzed: {report['summary']['total_analyzed']}")
    print(f"Files with URLs: {report['summary']['files_with_urls']}")
    print(f"Unique URLs found: {report['summary']['unique_urls']}")
    
    print("\n" + "=" * 50)
    print("UNIQUE URLs FOUND")
    print("=" * 50)
    for url in report['all_urls']:
        print(f"  - {url}")
    
    print("\n" + "=" * 50)
    print("FILES WITH NETWORK ACTIVITY")
    print("=" * 50)
    for result in results:
        if result["network_strings"] or result["urls"]:
            print(f"\nFile: {result['file']}")
            if result["urls"]:
                print(f"  URLs: {result['urls']}")
            if result["acer_strings"]:
                print(f"  Acer-related strings: {result['acer_strings'][:5]}")  # Limit output

if __name__ == "__main__":
    main()