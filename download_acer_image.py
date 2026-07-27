#!/usr/bin/env python3
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
