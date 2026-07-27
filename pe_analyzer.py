#!/usr/bin/env python3

import pefile
import capstone
import struct
import json
from typing import Dict, List, Optional, Any
from pathlib import Path

class MalwareAnalyzer:
    
    def __init__(self):
        self.disassembler = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    
    def analyze_pe(self, file_path: str) -> Dict:
        """Analyze PE file structure and imports"""
        if not Path(file_path).exists():
            return {"error": "File not found"}
        
        try:
            pe = pefile.PE(file_path)
            
            result = {
                "file_path": file_path,
                "basic_info": self._get_basic_info(pe),
                "imports": self._get_imports(pe),
                "exports": self._get_exports(pe),
                "sections": self._get_sections(pe),
                "network_functions": self._find_network_functions(pe),
                "update_functions": self._find_update_functions(pe)
            }
            
            pe.close()
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def _get_basic_info(self, pe) -> Dict:
        """Extract basic PE information"""
        return {
            "machine": hex(pe.FILE_HEADER.Machine),
            "entry_point": hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint),
            "image_base": hex(pe.OPTIONAL_HEADER.ImageBase),
            "subsystem": pe.OPTIONAL_HEADER.Subsystem,
            "characteristics": hex(pe.FILE_HEADER.Characteristics),
            "compilation_timestamp": pe.FILE_HEADER.TimeDateStamp
        }
    
    def _get_imports(self, pe) -> Dict:
        """Extract imported functions"""
        imports = {}
        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                dll_name = entry.dll.decode('utf-8')
                functions = []
                for imp in entry.imports:
                    if imp.name:
                        functions.append(imp.name.decode('utf-8'))
                imports[dll_name] = functions
        return imports
    
    def _get_exports(self, pe) -> List[str]:
        """Extract exported functions"""
        exports = []
        if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
            for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
                if exp.name:
                    exports.append(exp.name.decode('utf-8'))
        return exports
    
    def _get_sections(self, pe) -> List[Dict]:
        """Extract section information"""
        sections = []
        for section in pe.sections:
            sections.append({
                "name": section.Name.decode('utf-8').rstrip('\x00'),
                "virtual_address": hex(section.VirtualAddress),
                "virtual_size": hex(section.Misc_VirtualSize),
                "raw_size": hex(section.SizeOfRawData),
                "characteristics": hex(section.Characteristics)
            })
        return sections
    
    def _find_network_functions(self, pe) -> List[str]:
        """Find network-related imports"""
        network_keywords = ['http', 'url', 'download', 'upload', 'socket', 'connect', 'send', 'recv', 'internet']
        network_funcs = []
        
        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                for imp in entry.imports:
                    if imp.name:
                        func_name = imp.name.decode('utf-8').lower()
                        if any(keyword in func_name for keyword in network_keywords):
                            network_funcs.append({
                                "dll": entry.dll.decode('utf-8'),
                                "function": imp.name.decode('utf-8')
                            })
        return network_funcs
    
    def _find_update_functions(self, pe) -> List[str]:
        """Find update-related functions"""
        update_keywords = ['update', 'upgrade', 'download', 'install', 'version', 'check', 'fetch']
        update_funcs = []
        
        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                for imp in entry.imports:
                    if imp.name:
                        func_name = imp.name.decode('utf-8').lower()
                        if any(keyword in func_name for keyword in update_keywords):
                            update_funcs.append({
                                "dll": entry.dll.decode('utf-8'),
                                "function": imp.name.decode('utf-8')
                            })
        return update_funcs
    
    def disassemble_function(self, file_path: str, address: int, size: int = 128) -> List[Dict]:
        """Disassemble code at specific address"""
        try:
            pe = pefile.PE(file_path)
            va = pe.OPTIONAL_HEADER.ImageBase + address
            section = pe.get_section_by_rva(address)
            
            if not section:
                pe.close()
                return []
            
            data = section.get_data()
            instructions = []
            
            for insn in self.disassembler.disasm(data, va):
                instructions.append({
                    "address": hex(insn.address),
                    "bytes": insn.bytes.hex(),
                    "mnemonic": insn.mnemonic,
                    "op_str": insn.op_str
                })
                
                if len(instructions) >= size:
                    break
            
            pe.close()
            return instructions
        except Exception as e:
            return [{"error": str(e)}]
    
    def extract_strings(self, file_path: str) -> List[str]:
        """Extract printable strings from file"""
        strings = []
        counter = 0
        
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
                current_string = ""
                
                for byte in data:
                    if 32 <= byte <= 126:
                        current_string += chr(byte)
                        counter += 1
                    else:
                        if counter >= 4:
                            strings.append(current_string)
                        current_string = ""
                        counter = 0
                
                if counter >= 4:
                    strings.append(current_string)
            
            return strings[:1000]  # Limit to first 1000 strings
        except Exception as e:
            return [f"Error: {str(e)}"]
    
    def analyze_update_logic(self, file_path: str) -> Dict:
        """Analyze application for update logic"""
        analysis = self.analyze_pe(file_path)
        
        if "error" in analysis:
            return analysis
        
        update_analysis = {
            "file": file_path,
            "network_functions": analysis.get("network_functions", []),
            "update_functions": analysis.get("update_functions", []),
            "suspicious_strings": [],
            "url_patterns": []
        }
        
        # Look for URLs and update-related strings
        strings = self.extract_strings(file_path)
        for string in strings:
            string_lower = string.lower()
            if any(keyword in string_lower for keyword in ['http', 'https', 'ftp', 'update', 'download', 'version']):
                update_analysis["suspicious_strings"].append(string)
            
            if string.startswith(('http://', 'https://')):
                update_analysis["url_patterns"].append(string)
        
        return update_analysis