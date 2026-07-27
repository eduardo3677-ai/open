import requests
import re
import json
from typing import Dict, List, Optional, Tuple

class AcerUpdateAnalyzer:
    
    USER_AGENT = "Acer Update Agent/1.0"
    DEFAULT_HEADERS = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Accept-Language": "es-ES,es;q=0.9"
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)
        self.update_servers = [
            "global-download.acer.com",
            "us-one-client-update.ecs.acer.com",
            "eu-one-client-update.ecs.acer.com"
        ]
    
    def analyze_download_url(self, url: str) -> Dict:
        """Analyze Acer download URL structure"""
        result = {
            "url": url,
            "components": {},
            "parameters": {}
        }
        
        # Parse main components
        pattern = r"https://([^/]+)/GDFiles/([^/]+)/([^/]+)/([^/]+)"
        match = re.match(pattern, url)
        if match:
            result["components"] = {
                "domain": match.group(1),
                "category": match.group(2),
                "app_name": match.group(3),
                "file": match.group(4)
            }
        
        # Parse query parameters
        params = re.findall(r'(\w+)=([^&]+)', url)
        for key, val in params:
            result["parameters"][key] = val
        
        return result
    
    def check_index_servers(self) -> Dict:
        """Check potential update/index servers"""
        results = {}
        
        for server in self.update_servers:
            try:
                # Try common endpoints
                endpoints = [
                    "/update/index.json",
                    "/api/v1/updates", 
                    "/updates/index",
                    "/download/index"
                ]
                
                server_results = []
                for endpoint in endpoints:
                    url = f"https://{server}{endpoint}"
                    try:
                        response = self.session.get(url, timeout=10)
                        server_results.append({
                            "endpoint": endpoint,
                            "status": response.status_code,
                            "content_type": response.headers.get("content-type", "unknown")
                        })
                    except Exception as e:
                        server_results.append({
                            "endpoint": endpoint,
                            "error": str(e)
                        })
                
                results[server] = server_results
            except Exception as e:
                results[server] = {"error": str(e)}
        
        return results
    
    def search_factory_image(self, model: str = "ASPIRE A315-59") -> Dict:
        """Search for factory image download endpoints"""
        search_patterns = [
            f"/GDFiles/BIOS/BIOS/{model}",
            f"/GDFiles/OS/OS/{model}",
            f"/GDFiles/Recovery/Recovery/{model}"
        ]
        
        results = []
        for server in self.update_servers:
            for pattern in search_patterns:
                url = f"https://{server}{pattern}"
                # This would need actual network access to work properly
                results.append({
                    "server": server,
                    "pattern": pattern,
                    "potential_url": url
                })
        
        return {"model": model, "search_results": results}