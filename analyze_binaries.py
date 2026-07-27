#!/usr/bin/env python3
import pefile
import re
import os
import sys
from pathlib import Path

def extract_strings_from_binary(filepath, min_length=4):
    """Extract printable strings from a binary file"""
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        
        strings = []
        current_string = ""
        for byte in data:
            if 32 <= byte <= 126:  # printable ASCII
                current_string += chr(byte)
            else:
                if len(current_string) >= min_length:
                    strings.append(current_string)
                current_string = ""
        
        if len(current_string) >= min_length:
            strings.append(current_string)
            
        return strings
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def analyze_pe_file(filepath):
    """Analyze a PE file for download-related strings and patterns"""
    print(f"\n{'='*80}")
    print(f"Analyzing: {filepath}")
    print(f"{'='*80}")
    
    try:
        pe = pefile.PE(filepath)
        
        print(f"Entry Point: 0x{pe.OPTIONAL_HEADER.AddressOfEntryPoint:X}")
        print(f"Image Base: 0x{pe.OPTIONAL_HEADER.ImageBase:X}")
        print(f"Sections: {[section.Name.decode().strip('\x00') for section in pe.sections]}")
        
        # Extract strings
        strings = extract_strings_from_binary(filepath)
        
        # Look for download-related patterns
        download_keywords = [
            'download', 'update', 'http://', 'https://', 'ftp://',
            'url', 'uri', 'request', 'response', 'server',
            'content-type', 'user-agent', 'accept', 'post', 'get',
            'api', 'endpoint', 'session', 'cookie', 'header'
        ]
        
        relevant_strings = []
        for s in strings:
            s_lower = s.lower()
            if any(keyword in s_lower for keyword in download_keywords):
                relevant_strings.append(s)
        
        print(f"\nFound {len(relevant_strings)} potentially relevant strings:")
        
        # Group by patterns
        urls = [s for s in relevant_strings if 'http' in s.lower()]
        headers = [s for s in relevant_strings if any(h in s.lower() for h in ['user-agent', 'content-type', 'accept', 'cookie'])]
        download_terms = [s for s in relevant_strings if any(d in s.lower() for d in ['download', 'update', 'driver', 'firmware'])]
        
        if urls:
            print("\n  URLs found:")
            for url in urls[:20]:  # Limit to first 20
                print(f"    {url}")
        
        if headers:
            print("\n  HTTP Headers found:")
            for header in headers[:20]:
                print(f"    {header}")
        
        if download_terms:
            print("\n  Download/Update related strings:")
            for dt in download_terms[:20]:
                print(f"    {dt}")
        
        # Look for specific patterns in imports
        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            print("\n  Imports:")
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                print(f"    {entry.dll.decode()}")
        
        pe.close()
        
        return relevant_strings
        
    except Exception as e:
        print(f"Error analyzing PE file: {e}")
        return []

def find_key_executables(base_dir):
    """Find main executables that might contain download logic"""
    key_executables = []
    
    # Patterns for executables that likely contain download logic
    key_patterns = [
        '*Agent*.exe', '*Service*.exe', '*Center*.exe', 
        '*Sense*.exe', '*Update*.exe', '*Download*.exe',
        '*Setup*.exe'
    ]
    
    for pattern in key_patterns:
        for exe_path in Path(base_dir).rglob(pattern):
            if exe_path.is_file():
                key_executables.append(str(exe_path))
    
    return key_executables

def main():
    base_dir = "acer_analysis"
    
    if not os.path.exists(base_dir):
        print(f"Directory {base_dir} not found")
        return
    
    key_executables = find_key_executables(base_dir)
    
    print(f"Found {len(key_executables)} potentially relevant executables")
    
    for exe_path in key_executables[:10]:  # Analyze first 10 found
        analyze_pe_file(exe_path)

if __name__ == "__main__":
    main()