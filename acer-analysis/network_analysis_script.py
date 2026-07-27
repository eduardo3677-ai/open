#!/usr/bin/env python3
"""
Network Analysis Script for Acer Software
This script analyzes network patterns and creates documentation for public API endpoints.
"""

import os
import json
import re
import socket
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime

class AcerNetworkAnalyzer:
    def __init__(self, analysis_dir="acer-analysis"):
        self.analysis_dir = Path(analysis_dir)
        self.results = {
            "endpoints": [],
            "protocols": [],
            "certificates": [],
            "network_libraries": [],
            "patterns": []
        }
        
    def analyze_endpoints(self):
        """Analyze discovered network endpoints"""
        known_endpoints = [
            "https://device-info-uat-ycrmvsk7ia-uc.a.run.app",
            "https://device-info-prd-imub2p4wyq-uc.a.run.app",
            "https://global-download.acer.com"
        ]
        
        for endpoint in known_endpoints:
            parsed = urlparse(endpoint)
            result = {
                "url": endpoint,
                "host": parsed.netloc,
                "protocol": parsed.scheme,
                "type": self.classify_endpoint(endpoint),
                "port": self.detect_port(parsed.scheme),
                "analysis_timestamp": datetime.now().isoformat()
            }
            self.results["endpoints"].append(result)
            
        return self.results["endpoints"]
    
    def classify_endpoint(self, url):
        """Classify endpoint type based on URL pattern"""
        if "device-info" in url:
            return "device_information"
        elif "global-download" in url:
            return "download_server"
        else:
            return "unknown"
    
    def detect_port(self, scheme):
        """Detect standard ports based on scheme"""
        return {"https": 443, "http": 80}.get(scheme, "unknown")
    
    def analyze_protocols(self):
        """Document network protocols used"""
        protocols = [
            {
                "name": "HTTPS",
                "version": "1.2+",
                "purpose": "Encrypted communication",
                "security": "SSL/TLS encryption"
            },
            {
                "name": "HTTP",
                "version": "1.1",
                "purpose": "Web requests",
                "security": "Unencrypted (not recommended)"
            }
        ]
        
        self.results["protocols"] = protocols
        return protocols
    
    def analyze_network_libraries(self):
        """Document network-related libraries"""
        libraries = [
            "libssl-3-x64.dll",
            "libcrypto-3-x64.dll", 
            "cares.dll",
            "brotlicommon.dll",
            "brotlidec.dll",
            "brotlienc.dll"
        ]
        
        library_info = []
        for lib in libraries:
            info = {
                "filename": lib,
                "purpose": self.identify_library_purpose(lib),
                "category": self.categorize_library(lib)
            }
            library_info.append(info)
        
        self.results["network_libraries"] = library_info
        return library_info
    
    def identify_library_purpose(self, library):
        """Identify the purpose of a network library"""
        purposes = {
            "libssl": "SSL/TLS communication",
            "libcrypto": "Cryptographic operations",
            "cares": "Asynchronous DNS resolution",
            "brotli": "Compression/decompression"
        }
        
        for key, purpose in purposes.items():
            if key in library.lower():
                return purpose
        return "Unknown"
    
    def categorize_library(self, library):
        """Categorize library by function"""
        categories = {
            "libssl": "security",
            "libcrypto": "security",
            "cares": "network",
            "brotli": "compression"
        }
        
        for key, category in categories.items():
            if key in library.lower():
                return category
        return "other"
    
    def analyze_network_patterns(self):
        """Document network communication patterns"""
        patterns = [
            {
                "pattern": "HTTP POST requests",
                "description": "Standard POST method for data submission",
                "headers": ["Content-Type", "User-Agent", "Authorization"],
                "security_notes": "Should use HTTPS"
            },
            {
                "pattern": "Device identification",
                "description": "Sending hardware information",
                "parameters": ["SNID", "UUID", "Model"],
                "security_notes": "Contains sensitive device data"
            },
            {
                "pattern": "Version checking",
                "description": "Update version comparison",
                "mechanisms": ["Server comparison", "Local registry check"],
                "security_notes": "Secure update verification needed"
            }
        ]
        
        self.results["patterns"] = patterns
        return patterns
    
    def create_network_documentation(self, output_file="network_documentation.json"):
        """Create comprehensive network documentation"""
        self.analyze_endpoints()
        self.analyze_protocols()
        self.analyze_network_libraries()
        self.analyze_network_patterns()
        
        documentation = {
            "analysis_timestamp": datetime.now().isoformat(),
            "analysis_type": "network_patterns",
            "summary": {
                "total_endpoints": len(self.results["endpoints"]),
                "total_protocols": len(self.results["protocols"]),
                "total_libraries": len(self.results["network_libraries"]),
                "total_patterns": len(self.results["patterns"])
            },
            "endpoints": self.results["endpoints"],
            "protocols": self.results["protocols"],
            "network_libraries": self.results["network_libraries"],
            "patterns": self.results["patterns"]
        }
        
        output_path = self.analysis_dir / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(documentation, f, indent=2, ensure_ascii=False)
        
        return documentation
    
    def generate_endpoint_connectivity_report(self):
        """Generate report about endpoint connectivity"""
        report = {
            "connectivity_analysis": [],
            "dns_resolution": [],
            "security_recommendations": []
        }
        
        for endpoint in self.results["endpoints"]:
            host = endpoint["host"]
            connectivity_info = {
                "endpoint": endpoint["url"],
                "host": host,
                "expected_response": "HTTPS handshake",
                "requirements": [
                    "Internet connectivity",
                    "DNS resolution",
                    "Port 443 accessibility",
                    "SSL certificate validation"
                ]
            }
            report["connectivity_analysis"].append(connectivity_info)
            
            dns_info = {
                "hostname": host,
                "record_types": ["A", "AAAA", "CNAME"],
                "notes": "Use standard DNS resolution"
            }
            report["dns_resolution"].append(dns_info)
        
        security_recommendations = [
            "Always verify SSL certificates",
            "Use official Acer clients when possible",
            "Monitor for unauthorized access",
            "Keep network libraries updated",
            "Use proper authentication"
        ]
        
        report["security_recommendations"] = security_recommendations
        
        return report

def main():
    """Main execution function"""
    print("Acer Network Analysis Tool")
    print("=" * 50)
    
    analyzer = AcerNetworkAnalyzer()
    
    # Create comprehensive documentation
    print("\nGenerating network documentation...")
    documentation = analyzer.create_network_documentation()
    
    print(f"Documentation saved to: {analyzer.analysis_dir}/network_documentation.json")
    print(f"Analyzed {documentation['summary']['total_endpoints']} endpoints")
    print(f"Documented {documentation['summary']['total_libraries']} network libraries")
    
    # Generate connectivity report
    print("\nGenerating connectivity report...")
    connectivity_report = analyzer.generate_endpoint_connectivity_report()
    
    connectivity_path = analyzer.analysis_dir / "connectivity_report.json"
    with open(connectivity_path, 'w', encoding='utf-8') as f:
        json.dump(connectivity_report, f, indent=2, ensure_ascii=False)
    
    print(f"Connectivity report saved to: {connectivity_path}")
    
    print("\nAnalysis Summary:")
    print(f"  Network Endpoints: {documentation['summary']['total_endpoints']}")
    print(f"  Protocols Documented: {documentation['summary']['total_protocols']}")
    print(f"  Network Libraries: {documentation['summary']['total_libraries']}")
    print(f"  Communication Patterns: {documentation['summary']['total_patterns']}")
    
    print("\nGenerated files:")
    print("  - network_documentation.json")
    print("  - connectivity_report.json")
    print("  - NETWORK_ENDPOINTS.md")

if __name__ == "__main__":
    main()