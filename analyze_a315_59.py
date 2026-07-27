#!/usr/bin/env python3
"""
Script especializado para obtener archivos del modelo Acer A315-59 usando el SNID específico
"""

import requests
import json
import re
from typing import Dict, Optional, List
import time

class AcerA315Analyzer:
    """Analizador especializado para modelo A315-59"""
    
    def __init__(self, snid: str):
        self.snid = snid.strip()
        self.model = "A315-59"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "AcerDIAgent/1.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9"
        })
    
    def try_all_endpoints(self) -> Dict:
        """Intenta todos los endpoints conocidos con diferentes combinaciones"""
        results = {}
        
        endpoints = [
            "https://device-info-prd-imub2p4wyq-uc.a.run.app",
            "https://device-info-uat-ycrmvsk7ia-uc.a.run.app",
            "https://api-smartquery-int.acer.com",
            "https://api-az.cdp.acer.com",
            "https://download.acer.com/api/v1",
            "https://support.acer.com/api",
            "https://www.acer.com/api/v1"
        ]
        
        payload_variations = [
            {"snid": self.snid, "model": self.model},
            {"serial_number": self.snid, "model": self.model},
            {"snid": self.snid, "product_code": self.model},
            {"device_id": self.snid, "model": self.model},
            {"SNID": self.snid, "MODEL": self.model},
            {self.snid: self.model}
        ]
        
        for endpoint in endpoints:
            for payload in payload_variations:
                result = self.try_endpoint(endpoint, payload)
                if result:
                    key = f"{endpoint}_{str(payload)}"
                    results[key] = result
        
        return results
    
    def try_endpoint(self, endpoint: str, payload: Dict) -> Optional[Dict]:
        """Intenta un endpoint específico con el payload dado"""
        for method in ['GET', 'POST']:
            for content_type in ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data']:
                headers = self.session.headers.copy()
                headers["Content-Type"] = content_type
                
                try:
                    if method == 'GET':
                        response = self.session.get(endpoint, params=payload, headers=headers, timeout=30)
                    else:
                        if content_type == 'application/json':
                            response = self.session.post(endpoint, json=payload, headers=headers, timeout=30)
                        else:
                            response = self.session.post(endpoint, data=payload, headers=headers, timeout=30)
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            return {
                                'method': method,
                                'content_type': content_type,
                                'payload': payload,
                                'response': data,
                                'status_code': response.status_code,
                                'headers': dict(response.headers)
                            }
                        except:
                            return {
                                'method': method,
                                'content_type': content_type,
                                'payload': payload,
                                'response': response.text,
                                'status_code': response.status_code,
                                'headers': dict(response.headers)
                            }
                    
                except Exception as e:
                    continue
        
        return None
    
    def extract_download_urls(self, response_data: str) -> List[str]:
        """Extrae URLs de descarga de la respuesta"""
        url_pattern = re.compile(r'https?://[^\s<>"{}|\\^`[\]]+')
        urls = url_pattern.findall(response_data)
        
        filter_keywords = ['download', 'image', 'recovery', 'factory', 'iso', 'zip', 'exe', 'msi']
        filtered_urls = [url for url in urls if any(keyword in url.lower() for keyword in filter_keywords)]
        
        return filtered_urls
    
    def analyze_response_structure(self, data: Dict) -> Dict:
        """Analiza la estructura de respuesta para encontrar patrones"""
        if isinstance(data, dict):
            return {
                'keys': list(data.keys()),
                'has_download_url': any('url' in str(key).lower() for key in data.keys()),
                'has_file_info': any('file' in str(key).lower() or 'download' in str(key).lower() for key in data.keys())
            }
        return data

def main():
    """Función principal"""
    snid = "NXK6TAL019416025803400"
    model = "A315-59"
    
    print(f"╔═══════════════════════════════════════════════════════════════════╗")
    print(f"║  Analizador Especializado Acer A315-59                             ║")
    print(f"║  SNID: {snid}                                             ║")
    print(f"╚═══════════════════════════════════════════════════════════════════╝")
    
    analyzer = AcerA315Analyzer(snid)
    
    print(f"\n🔄 Analizando endpoints para modelo {model}...")
    results = analyzer.try_all_endpoints()
    
    print(f"\n📊 Resultados obtenidos: {len(results)} respuestas exitosas")
    
    successful_requests = 0
    for key, result in results.items():
        successful_requests += 1
        print(f"\n--- Request #{successful_requests} ---")
        print(f"Endpoint: {key.split('_')[0]}")
        print(f"Método: {result['method']}")
        print(f"Content-Type: {result['content_type']}")
        print(f"Payload: {result['payload']}")
        print(f"Status: {result['status_code']}")
        
        response_str = json.dumps(result['response'], indent=2) if isinstance(result['response'], dict) else result['response']
        print(f"Response: {response_str[:500]}...")
        
        # Extraer URLs de descarga
        urls = analyzer.extract_download_urls(response_str)
        if urls:
            print(f"🔗 URLs de descarga encontradas:")
            for url in urls:
                print(f"  - {url}")
    
    # Guardar resultados completos
    output_file = "a315_59_analysis_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Resultados completos guardados en: {output_file}")
    
    # Resumen de hallazgos
    print(f"\n📋 RESUMEN:")
    print(f"- Total deEndpoints probados: {len(['https://device-info-prd-imub2p4wyq-uc.a.run.app', 'https://device-info-uat-ycrmvsk7ia-uc.a.run.app', 'https://api-smartquery-int.acer.com', 'https://api-az.cdp.acer.com', 'https://download.acer.com/api/v1', 'https://support.acer.com/api', 'https://www.acer.com/api/v1'])}")
    print(f"- Solicitudes exitosas: {successful_requests}")
    print(f"- Model: {model}")
    print(f"- SNID: {snid}")

if __name__ == "__main__":
    main()