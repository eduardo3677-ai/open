#!/usr/bin/env python3
import pefile
import re
import os
import sys
from pathlib import Path

def extract_url_patterns(filepath):
    """Extract URL patterns and server endpoints from binary"""
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        
        # Strings with longer patterns for URLs
        url_patterns = []
        current_string = ""
        for byte in data:
            if 32 <= byte <= 126:  # printable ASCII
                current_string += chr(byte)
            else:
                if len(current_string) >= 8:
                    # Look for URL-like patterns
                    if re.search(r'https?://', current_string):
                        url_patterns.append(current_string)
                current_string = ""
        
        # Also check the last string
        if len(current_string) >= 8 and re.search(r'https?://', current_string):
            url_patterns.append(current_string)
            
        return url_patterns
    except Exception as e:
        print(f"Error extracting URLs: {e}")
        return []

def analyze_factory_image_servers(filepath):
    """Look for factory image download servers and configurations"""
    print(f"\n{'='*80}")
    print(f"Searching for factory image download patterns in: {filepath}")
    print(f"{'='*80}")
    
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        
        # Search for specific patterns
        patterns = {
            'Acer servers': [
                rb'acer\.com',
                rb'global-download\.acer\.com',
                rb'acer-cdn',
                rb'acer-cloud',
                rb'acer-update',
            ],
            'Factory image keywords': [
                rb'factory',
                rb'recovery',
                rb'image',
                rb'partition',
                rb'restore',
                rb'backup',
                rb'iso',
            ],
            'Download endpoints': [
                rb'download',
                rb'update',
                rb'firmware',
                rb'driver',
                rb'content',
            ],
            'Config files': [
                rb'\.xml',
                rb'\.json',
                rb'\.config',
                rb'\.ini',
            ],
        }
        
        found_patterns = {}
        for category, keywords in patterns.items():
            found = []
            for keyword in keywords:
                # Find all matches
                matches = re.finditer(keyword, data)
                for match in matches:
                    # Get context around the match
                    start = max(0, match.start() - 100)
                    end = min(len(data), match.end() + 100)
                    context = data[start:end]
                    
                    # Try to extract readable strings from context
                    try:
                        context_str = context.decode('ascii', errors='ignore')
                        found.append(context_str)
                    except:
                        pass
            
            if found:
                found_patterns[category] = found[:5]  # Limit to 5 examples
        
        if found_patterns:
            print("\nFound patterns:")
            for category, matches in found_patterns.items():
                print(f"\n  {category}:")
                for match in matches:
                    # Clean up the display
                    cleaned = match.replace('\n', ' ').replace('\r', ' ').strip()
                    if len(cleaned) > 200:
                        cleaned = cleaned[:200] + "..."
                    print(f"    {cleaned}")
        
        # Extract all URLs found
        urls = extract_url_patterns(filepath)
        if urls:
            print(f"\n  URLs found ({len(urls)}):")
            unique_urls = list(set(urls[:10]))  # First 10 unique URLs
            for url in unique_urls:
                print(f"    {url}")
        
        return found_patterns
        
    except Exception as e:
        print(f"Error analyzing factory image patterns: {e}")
        return {}

def main():
    base_dir = "acer_analysis"
    
    if not os.path.exists(base_dir):
        print(f"Directory {base_dir} not found")
        return
    
    # Focus on executables that are likely to contain server information
    key_files = [
        "acer_analysis/AcerSense_Acer_5.0.1752_W11x64/AcerSense5_RC18_ARM_RC6_5.0.1752/AcerDIAgent/AcerDIAgent.exe",
        "acer_analysis/AcerSense_Acer_5.0.1752_W11x64/AcerSense5_RC18_ARM_RC6_5.0.1752/AcerCCAgent/AcerCCAgent.exe",
        "acer_analysis/AcerSense_Acer_5.0.1752_W11x64/AcerSense5_RC18_ARM_RC6_5.0.1752/AcerQAAgent/AcerQAAgent.exe",
        "acer_analysis/Acer Care Center_v4.00.3060 MSFT SIGNED_20260510/Setup.exe",
    ]
    
    for filepath in key_files:
        if os.path.exists(filepath):
            analyze_factory_image_servers(filepath)

if __name__ == "__main__":
    main()