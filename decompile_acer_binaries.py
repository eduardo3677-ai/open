#!/usr/bin/env python3
import subprocess
import re
import os
import sys
import json
from pathlib import Path
from urllib.parse import urlparse
from typing import Dict, List, Tuple, Any

class AcerBinaryAnalyzer:
    def __init__(self, base_dir="acer_binaries"):
        self.base_dir = Path(base_dir)
        self.results: Dict[str, Any] = {
            'executables': {},
            'dlls': {},
            'APIs': {},
            'credentials': [],
            'download_logic': {},
            'headers': [],
            'endpoints': []
        }
        
    def check_tools_available(self) -> bool:
        """Check if required analysis tools are available"""
        tools = ['ghidraHeadless', 'strings', 'objdump', 'radare2', 'r2']
        available = []
        
        for tool in tools:
            try:
                subprocess.run([tool, '--help'], capture_output=True, timeout=2)
                available.append(tool)
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue
                
        return available
    
    def decompile_executable(self, exe_path: str, tool='ghidra') -> Dict[str, Any]:
        """Decompile executable using available tools"""
        exe_info = {
            'path': str(exe_path),
            'size': os.path.getsize(exe_path),
            'decompilation': {},
            'imports': [],
            'exports': [],
            'strings': [],
            'download_logic': {}
        }
        
        print(f"Decompiling: {exe_path}")
        
        # Extract using multiple methods
        exe_info.update(self.extract_basic_info(exe_path))
        exe_info['strings'] = self.extract_strings(exe_path)
        exe_info['imports'], exe_info['exports'] = self.extract_imports_exports(exe_path)
        
        # Analyze for download logic
        exe_info['download_logic'] = self.analyze_download_logic(exe_info['strings'], exe_info['imports'])
        
        return exe_info
    
    def extract_basic_info(self, exe_path: str) -> Dict[str, Any]:
        """Extract basic PE/ELF information using objdump"""
        info = {}
        
        try:
            # PE header info
            proc = subprocess.run(
                ['objdump', '-x', exe_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if proc.returncode == 0:
                lines = proc.stdout.split('\n')
                for line in lines:
                    if 'Entry point' in line:
                        info['entry_point'] = line.strip()
                    elif 'image base' in line.lower() or 'start address' in line.lower():
                        info['image_base'] = line.strip()
                        
        except Exception as e:
            print(f"Error extracting basic info: {e}")
            
        return info
    
    def extract_strings(self, exe_path: str, min_length=4) -> List[str]:
        """Extract strings using strings command"""
        strings = []
        
        try:
            proc = subprocess.run(
                ['strings', '-n', str(min_length), exe_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if proc.returncode == 0:
                strings = proc.stdout.split('\n')
                
        except Exception as e:
            print(f"Error extracting strings: {e}")
            
        return strings
    
    def extract_imports_exports(self, exe_path: str) -> Tuple[List[str], List[str]]:
        """Extract imports and exports using objdump"""
        imports = []
        exports = []
        
        try:
            # Imports
            proc = subprocess.run(
                ['objdump', '-p', exe_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if proc.returncode == 0:
                lines = proc.stdout.split('\n')
                current_dll = None
                
                for line in lines:
                    line = line.strip()
                    if 'DLL Name:' in line:
                        current_dll = line.replace('DLL Name:', '').strip()
                    elif line and current_dll and 'IAT' not in line and 'Hint' not in line:
                        imports.append(f"{current_dll}:{line}")
                        
        except Exception as e:
            print(f"Error extracting imports/exports: {e}")
            
        return imports, exports
    
    def analyze_download_logic(self, strings: List[str], imports: List[str]) -> Dict[str, Any]:
        """Analyze strings and imports for download-related logic"""
        analysis = {
            'API_endpoints': [],
            'HTTP_methods': [],
            'headers': [],
            'authentication': [],
            'download_functions': [],
            'credentials': []
        }
        
        # Compile regex patterns
        url_pattern = re.compile(r'https?://[^\s<>"{}|\\^`[\]]+')
        func_pattern = re.compile(r'(Download|Update|Request|Response|Connect|Auth|Login|Session|Cookie|Header|Post|Get|Put|Delete).{0,50}', re.IGNORECASE)
        auth_pattern = re.compile(r'(token|api[_-]?key|password|username|credential|secret|bearer)[\s:=]+.{0,50}', re.IGNORECASE)
        header_pattern = re.compile(r'([A-Za-z-]+):\s*([^\s]+)', re.IGNORECASE)
        
        # Analyze strings
        for string in strings:
            # URLs
            urls = url_pattern.findall(string)
            for url in urls:
                if any(keyword in url.lower() for keyword in ['api', 'server', 'download', 'update', 'service']):
                    analysis['API_endpoints'].append(url)
                    
            # HTTP methods
            for method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD']:
                if string == method or string == method.lower():
                    analysis['HTTP_methods'].append(method)
                    
            # HTTP headers
            headers = header_pattern.findall(string)
            for header_name, header_value in headers:
                analysis['headers'].append(f"{header_name}: {header_value}")
                
            # Authentication patterns
            auth_matches = auth_pattern.findall(string)
            for match in auth_matches:
                analysis['authentication'].append(match)
                analysis['credentials'].append(string)
                
            # Download functions
            func_matches = func_pattern.findall(string)
            for match in func_matches:
                analysis['download_functions'].append(match)
        
        # Analyze imports for WinINET functions
        wininet_functions = [
            'HttpOpenRequest', 'HttpSendRequest', 'HttpEndRequest', 
            'InternetOpen', 'InternetConnect', 'HttpQueryInfo',
            'InternetReadFile', 'InternetSetOption', 'InternetCrackUrl'
        ]
        
        for imp in imports:
            for func in wininet_functions:
                if func.lower() in imp.lower():
                    analysis['download_functions'].append(f"WININET:{imp}")
                    
        return analysis
    
    def analyze_dll(self, dll_path: str) -> Dict[str, Any]:
        """Analyze DLL for download-related functionality"""
        print(f"Analyzing DLL: {dll_path}")
        
        dll_info = {
            'path': str(dll_path),
            'size': os.path.getsize(dll_path),
            'exports': [],
            'functions': []
        }
        
        try:
            proc = subprocess.run(
                ['objdump', '-p', dll_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if proc.returncode == 0:
                lines = proc.stdout.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('[') and 'DLL' not in line:
                        dll_info['functions'].append(line)
                        
        except Exception as e:
            print(f"Error analyzing DLL: {e}")
            
        return dll_info
    
    def extract_aspx_from_exe(self, exe_path: str) -> List[str]:
        """Extract embedded aspx and web resources from executable"""
        aspx_content = []
        
        try:
            # Use strings to find web content
            strings = self.extract_strings(exe_path, min_length=10)
            
            for string in strings:
                # Look for ASPX/HTML content indicators
                if any(indicator in string.upper() for indicator in ['ASPX', '.ASPX', 'WEBFORM', 'ASP.NET']):
                    aspx_content.append(string)
                    
                # Look for HTML/XML content
                if string.startswith('<') and '>' in string:
                    if len(string) > 20 and any(tag in string.upper() for tag in ['HTML', 'BODY', 'FORM', 'ASP:']):
                        aspx_content.append(string)
                        
        except Exception as e:
            print(f"Error extracting ASPX content: {e}")
            
        return aspx_content
    
    def find_download_headers_and_body(self, exe_info: Dict[str, Any]) -> Dict[str, Any]:
        """Extract HTTP request/response patterns including headers and body structure"""
        patterns = {
            'request_headers': [],
            'response_headers': [],
            'request_body_patterns': [],
            'url_parameters': [],
            'content_types': []
        }
        
        strings = exe_info.get('strings', [])
        
        # Header patterns
        header_patterns = [
            r'Content-Type:\s*([^\s]+)',
            r'User-Agent:\s*([^\n]+)',
            r'Accept:\s*([^\n]+)',
            r'Authorization:\s*([^\n]+)',
            r'Cookie:\s*([^\n]+)',
            r'X-[A-Za-z-]+:\s*([^\n]+)'
        ]
        
        for string in strings:
            for pattern in header_patterns:
                match = re.search(pattern, string, re.IGNORECASE)
                if match:
                    patterns['request_headers'].append(match.group(0))
                    
                    if 'Content-Type' in match.group(0):
                        patterns['content_types'].append(match.group(1))
        
        # Body patterns look for JSON, XML, form-data structures
        body_patterns = [
            r'\{[^{}]*"device"[^{}]*\}',
            r'<device[^>]*>.*</device>',
            r'model=[^&\s]+&',
            r'serial=[^&\s]+&',
            r'format=[^&\s]+&',
            r'action=[^&\s]+&'
        ]
        
        for string in strings:
            for pattern in body_patterns:
                matches = re.findall(pattern, string, re.IGNORECASE)
                patterns['request_body_patterns'].extend(matches)
                
        # URL parameters
        url_pattern = re.compile(r'[?&]([a-z_]+)=([^&\s]+)', re.IGNORECASE)
        for string in strings:
            if 'http' in string.lower():
                params = url_pattern.findall(string)
                for param_name, param_value in params:
                    patterns['url_parameters'].append(f"{param_name}={param_value}")
                    
        return patterns
    
    def generate_download_script(self, output_file="download_acer_image.py") -> str:
        """Generate a Python script based on discovered patterns"""
        script_content = '''#!/usr/bin/env python3
import requests
import json
from typing import Dict, Optional

class AcerImageDownloader:
    """Download Acer factory recovery images using discovered API patterns"""
    
    BASE_URL = "https://device-info-prd-imub2p4wyq-uc.a.run.app"
    FALLBACK_URL = "https://device-info-uat-ycrmvsk7ia-uc.a.run.app"
    
    def __init__(self):
        self.session = requests.Session()
        
    def get_device_info(self, device_model: str, snid: Optional[str] = None) -> Dict:
        """Query device information API"""
        headers = {
            "User-Agent": "AcerDIAgent/1.0",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "model": device_model,
            "format": "factory_image"
        }
        
        if snid:
            payload["snid"] = snid
            
        try:
            response = self.session.post(
                self.BASE_URL,
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Primary API failed: {e}")
            
        try:
            response = self.session.post(
                self.FALLBACK_URL,
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Fallback API failed: {e}")
            return {"error": str(e)}
    
    def download_factory_image(self, device_model: str, save_path: str = "./") -> bool:
        """Download factory image for specified device"""
        print(f"Querying factory image for: {device_model}")
        
        device_info = self.get_device_info(device_model)
        
        if "download_url" in device_info:
            download_url = device_info["download_url"]
            print(f"Download URL: {download_url}")
            
            try:
                response = self.session.get(download_url, stream=True)
                response.raise_for_status()
                
                filename = download_url.split("/")[-1] or f"{device_model.replace(' ', '_')}_factory.zip"
                filepath = save_path / filename
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            
                print(f"Downloaded to: {filepath}")
                return True
                
            except Exception as e:
                print(f"Download failed: {e}")
                return False
                
        print("No download URL found in response")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) >= 2:
        device_model = " ".join(sys.argv[1:])
        downloader = AcerImageDownloader()
        downloader.download_factory_image(device_model)
    else:
        print("Usage: python download_acer_image.py <device_model>")
        print("Example: python download_acer_image.py ASPIRE A315-59")
'''
        
        with open(output_file, 'w') as f:
            f.write(script_content)
            
        return script_content
    
    def analyze_all(self) -> Dict[str, Any]:
        """Perform complete analysis of Acer executables and DLLs"""
        executables_to_analyze = ['AcerDIAgent.exe', 'AcerCCAgent.exe', 'AcerQAAgent.exe']
        
        # Analyze executables
        for exe_name in executables_to_analyze:
            exe_path = self.base_dir / exe_name
            if exe_path.exists():
                self.results['executables'][exe_name] = self.decompile_executable(str(exe_path))
                self.results['executables'][exe_name]['aspx_content'] = self.extract_aspx_from_exe(str(exe_path))
                self.results['executables'][exe_name]['http_patterns'] = self.find_download_headers_and_body(self.results['executables'][exe_name])
            else:
                print(f"Executable not found: {exe_path}")
        
        # Analyze DLLs
        dll_pattern = ['*.dll', 'WinINET.dll', 'CRYPT32.dll']
        for pattern in dll_pattern:
            for dll_path in self.base_dir.rglob(pattern):
                if dll_path.is_file():
                    dll_name = dll_path.name
                    self.results['dlls'][dll_name] = self.analyze_dll(str(dll_path))
        
        # Compile discovered patterns
        self.compile_discovered_patterns()
        
        # Generate download script
        self.generate_download_script()
        
        return self.results
    
    def compile_discovered_patterns(self):
        """Compile discovered patterns into usable format"""
        all_headers = []
        all_endpoints = []
        all_credentials = []
        
        for exe_name, exe_data in self.results['executables'].items():
            download_logic = exe_data.get('download_logic', {})
            http_patterns = exe_data.get('http_patterns', {})
            
            all_headers.extend(download_logic.get('headers', []))
            all_endpoints.extend(download_logic.get('API_endpoints', []))
            all_headers.extend(http_patterns.get('request_headers', []))
            all_credentials.extend(download_logic.get('credentials', []))
        
        self.results['headers'] = list(set(all_headers))
        self.results['endpoints'] = list(set(all_endpoints))
        self.results['credentials'] = list(set(all_credentials))
        
        print(f"Found {len(self.results['headers'])} unique headers")
        print(f"Found {len(self.results['endpoints'])} unique endpoints")
        print(f"Found {len(self.results['credentials'])} potential credentials")

def main():
    """Main execution function"""
    analyzer = AcerBinaryAnalyzer()
    
    # Check for available tools
    tools = analyzer.check_tools_available()
    print(f"Available analysis tools: {tools}")
    
    # Perform analysis
    results = analyzer.analyze_all()
    
    # Save results to JSON
    with open('acer_decompilation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("Analysis complete. Results saved to acer_decompilation_results.json")
    print("Download script generated: download_acer_image.py")

if __name__ == "__main__":
    main()