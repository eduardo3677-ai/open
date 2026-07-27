#!/usr/bin/env python3
"""
Script de análisis avanzado para obtener archivos del A315-59 con SNID NXK6TAL019416025803400
Intenta múltiples métodos de autenticación y análisis de contenido
"""

import requests
import json
import re
import os
import time
from urllib.parse import urlparse, parse_qs, urljoin
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Tuple

class AdvancedA31559Analyzer:
    """Analizador avanzado para A315-59 con SNID específico"""
    
    SNID = "NXK6TAL019416025803400"
    MODEL = "A315-59"
    
    BASE_ENDPOINTS = [
        "https://support.acer.com/api",
        "https://api.smrd.acer.com",
        "https://api.acer.com/api/v2",
        "https://download.acer.com/api",
        "https://driver.acer.com/api",
        "https://service.acer.com/api"
    ]
    
    USER_AGENTS = [
        "AcerDIAgent/1.0",
        "AcerCCAgent/1.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    ]
    
    def __init__(self):
        self.session = requests.Session()
        self.results = []
        
    def try_direct_file_endpoints(self):
        """Intenta endpoints directos para archivos de recuperación"""
        endpoints = [
            f"https://download.acer.com/{self.MODEL}/recovery",
            f"https://download.acer.com/{self.MODEL}/factory_image",
            f"https://download.acer.com/{self.MODEL}/recover",
            f"https://download.acer.com/Service/{self.MODEL}/download",
            f"https://download.acer.com/download/drivers/{self.MODEL}",
            f"https://download.acer.com/Drivers/Download/{self.MODEL}",
            f"https://download.acer.com/GD/Model/{self.MODEL}",
            f"https://download.acer.com/ac/Download/{self.MODEL}",
            f"https://download.acer.com/pc/{self.MODEL}",
            f"https://download.acer.com/notebook/{self.MODEL}",
            f"https://download.acer.com/laptop/{self.MODEL}",
            f"https://download.acer.com/aspire/{self.MODEL}",
            f"https://download.acer.com/win10/{self.MODEL}",
            f"https://download.acer.com/win11/{self.MODEL}",
            f"https://download.acer.com/system/{self.MODEL}",
            f"https://download.acer.com/BIOS/{self.MODEL}",
            f"https://download.acer.com/Firmware/{self.MODEL}",
            f"https://download.acer.com/RecoveryUSB/{self.MODEL}",
            f"https://download.acer.com/Recovery/{self.MODEL}",
            f"https://download.acer.com/ISO/{self.MODEL}",
            f"https://download.acer.com/ISO/Recovery/{self.MODEL}",
            f"https://download.acer.com/ISO/Factory/{self.MODEL}",
            f"https://download.acer.com/ISO/System/{self.MODEL}",
            f"https://download.acer.com/windows/{self.MODEL}",
            f"https://download.acer.com/windows10/{self.MODEL}",
            f"https://download.acer.com/windows11/{self.MODEL}",
            f"https://download.acer.com/download/system/{self.MODEL}",
            f"https://download.acer.com/download/recovery/{self.MODEL}",
            f"https://download.acer.com/download/factory/{self.MODEL}",
            f"https://download.acer.com/download/iso/{self.MODEL}",
            f"https://download.acer.com/download/drivers/{self.MODEL}",
            f"https://download.acer.com/download/app/{self.MODEL}",
            f"https://download.acer.com/download/utility/{self.MODEL}",
            f"https://download.acer.com/download/tools/{self.MODEL}"
        ]
        
        for endpoint in endpoints:
            for user_agent in self.USER_AGENTS:
                headers = {
                    "User-Agent": user_agent,
                    "Accept": "*/*"
                }
                
                try:
                    response = self.session.get(endpoint, headers=headers, timeout=10)
                    
                    if response.status_code in [200, 302, 301]:
                        result = {
                            "endpoint": endpoint,
                            "status_code": response.status_code,
                            "headers": dict(response.headers),
                            "content_type": response.headers.get('Content-Type', ''),
                            "content_length": len(response.content),
                            "success": True
                        }
                        
                        if response.status_code in [301, 302]:
                            result['redirect_url'] = response.headers.get('Location', '')
                        
                        content_preview = response.text[:500] if len(response.content) < 500 else response.text[:500]
                        result['content_preview'] = content_preview
                        
                        self.results.append(result)
                        print(f"✓ {endpoint} - Status: {response.status_code} - Content-Type: {result['content_type']}")
                        
                except Exception as e:
                    result = {
                        "endpoint": endpoint,
                        "error": str(e),
                        "success": False
                    }
                    self.results.append(result)
                    print(f"✗ {endpoint} - Error: {e}")
                    
                time.sleep(0.5)
    
    def try_api_with_different_formats(self):
        """Intenta API con diferentes formatos de parámetros"""
        parameters = [
            {"snid": self.SNID, "model": self.MODEL},
            {"SNID": self.SNID, "MODEL": self.MODEL},
            {"serial_number": self.SNID, "device_model": self.MODEL},
            {"deviceId": self.SNID, "modelId": self.MODEL},
            {"snid": self.SNID, "product": self.MODEL},
            {"SNID": self.SNID, "PRODUCT": self.MODEL},
            {"DeviceSN": self.SNID, "Model": self.MODEL},
            {"dev": self.SNID, "mod": self.MODEL},
            {"s": self.SNID, "m": self.MODEL},
            {self.SNID: self.MODEL},
            {f"Acer{self.SNID}": self.MODEL},
            {"action": "download", "snid": self.SNID, "model": self.MODEL},
            {"operation": "get_image", "snid": self.SNID, "model": self.MODEL},
            {"request": "recovery_image", "snid": self.SNID, "model": self.MODEL},
            {"type": "download", "snid": self.SNID, "model": self.MODEL}
        ]
        
        for base_url in self.BASE_ENDPOINTS:
            for params in parameters:
                for http_method in ['GET', 'POST']:
                    for content_type in ['application/json', 'application/x-www-form-urlencoded']:
                        headers = {
                            "User-Agent": "AcerDIAgent/1.0",
                            "Content-Type": content_type
                        }
                        
                        try:
                            if http_method == 'GET':
                                response = self.session.get(base_url, params=params, headers=headers, timeout=10)
                            else:
                                if content_type == 'application/json':
                                    response = self.session.post(base_url, json=params, headers=headers, timeout=10)
                                else:
                                    response = self.session.post(base_url, data=params, headers=headers, timeout=10)
                            
                            if response.status_code != 404:
                                result = {
                                    "endpoint": base_url,
                                    "method": http_method,
                                    "content_type": content_type,
                                    "params": params,
                                    "status_code": response.status_code,
                                    "response_headers": dict(response.headers),
                                    "success": True
                                }
                                
                                try:
                                    result['json_response'] = response.json()
                                except:
                                    result['html_response'] = response.text[:1000]
                                
                                self.results.append(result)
                                
                                if response.status_code == 200:
                                    print(f"✓ {base_url} {http_method} - Found response with params {params}")
                                    
                        except Exception as e:
                            continue
                            
                        time.sleep(0.5)
    
    def parse_for_download_links(self, html_content):
        """Analiza contenido HTML buscando enlaces de descarga"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            if any(keyword in href.lower() for keyword in ['download', 'file', 'zip', 'iso', 'exe', 'recovery', 'image', 'factory']):
                links.append(href)
        
        return links
    
    def try_sitemap_discovery(self):
        """Intenta descubrir sitemaps y archivos robots.txt"""
        discovery_urls = [
            "https://www.acer.com/sitemap.xml",
            "https://support.acer.com/sitemap.xml",
            "https://download.acer.com/sitemap.xml",
            "https://www.acer.com/robots.txt",
            "https://download.acer.com/robots.txt",
            f"https://download.acer.com/{self.MODEL}/",
            f"https://download.acer.com/{self.MODEL}/drivers/",
            f"https://download.acer.com/{self.MODEL}/recovery/"
        ]
        
        for url in discovery_urls:
            try:
                response = self.session.get(url, timeout=15)
                
                if response.status_code == 200:
                    result = {
                        "discovery_url": url,
                        "status_code": response.status_code,
                        "content_length": len(response.content),
                        "content_type": response.headers.get('Content-Type', ''),
                        "success": True
                    }
                    
                    if 'xml' in url:
                        result['sitemap_content'] = response.text[:2000]
                    elif 'txt' in url:
                        result['robots_content'] = response.text
                    else:
                        links = self.parse_for_download_links(response.text)
                        if links:
                            result['found_links'] = links
                            print(f"✓ {url} - Found {len(links)} potential download links")
                    
                    self.results.append(result)
                    
            except Exception as e:
                result = {
                    "discovery_url": url,
                    "error": str(e),
                    "success": False
                }
                self.results.append(result)
    
    def try_json_with_different_structure(self):
        """Intenta estructuras JSON alternativas"""
        endpoint = "https://support.acer.com/api"
        
        json_structures = [
            {"device": {"snid": self.SNID, "model": self.MODEL}},
            {"product": {"serial": self.SNID, "model": self.MODEL}},
            {"query": {"snid": self.SNID, "model": self.MODEL}},
            {"request": {"device_id": self.SNID, "model": self.MODEL}},
            {"data": {"snid": self.SNID, "model": self.MODEL}},
            {"deviceInfo": {"SNID": self.SNID, "MODELO": self.MODEL}},
            {"asset": {"SNID": self.SNID, "PROJECT": self.MODEL}},
            {"machine": {"sn": self.SNID, "model": self.MODEL}},
            {"system": {"snid": self.SNID, "model": self.MODEL, "action": "download"}},
            {"download": {"snid": self.SNID, "model": self.MODEL, "type": "recovery"}}
        ]
        
        for structure in json_structures:
            headers = {
                "User-Agent": "AcerDIAgent/1.0",
                "Content-Type": "application/json"
            }
            
            try:
                response = self.session.post(endpoint, json=structure, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    try:
                        json_response = response.json()
                        result = {
                            "endpoint": endpoint,
                            "structure": structure,
                            "status_code": response.status_code,
                            "json_response": json_response,
                            "success": True
                        }
                        self.results.append(result)
                        print(f"✓ JSON structure worked: {structure}")
                        
                    except:
                        result = {
                            "endpoint": endpoint,
                            "structure": structure,
                            "status_code": response.status_code,
                            "response_length": len(response.content),
                            "success": True
                        }
                        self.results.append(result)
                        
            except Exception as e:
                continue
                
            time.sleep(0.5)
    
    def analyze_results(self):
        """Analiza los resultados encontrados"""
        successful = [r for r in self.results if r.get('success')]
        json_responses = [r for r in successful if 'json_response' in r]
        redirects = [r for r in successful if 'redirect_url' in r]
        
        print(f"\n📊 ANÁLISIS DE RESULTADOS:")
        print(f"Total de intentos: {len(self.results)}")
        print(f"Respuestas exitosas: {len(successful)}")
        print(f"Respuestas JSON: {len(json_responses)}")
        print(f"Redirecciones: {len(redirects)}")
        
        if json_responses:
            print(f"\n🔍 RESPUESTAS JSON ENCONTRADAS:")
            for i, response in enumerate(json_responses, 1):
                print(f"{i}. {response.get('endpoint', 'Unknown endpoint')}")
                print(f"   Params: {response.get('params', response.get('structure', 'Unknown'))}")
                print(f"   Response: {json.dumps(response['json_response'], indent=2)[:500]}")
        
        if redirects:
            print(f"\n🔀 REDIRECCIONES ENCONTRADAS:")
            for i, redirect in enumerate(redirects, 1):
                print(f"{i}. {redirect['endpoint']} -> {redirect.get('redirect_url', 'Unknown')}")
        
    def save_results(self):
        """Guarda los resultados en un archivo JSON"""
        results_file = f"a315_59_advanced_results_{int(time.time())}.json"
        
        summary = {
            "device": {
                "model": self.MODEL,
                "snid": self.SNID
            },
            "total_attempts": len(self.results),
            "successful_attempts": len([r for r in self.results if r.get('success')]),
            "results": self.results
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Resultados guardados en: {results_file}")
        return results_file

def main():
    """Función principal de ejecución"""
    
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║  Analizador Avanzado A315-59                                      ║
║  SNID: NXK6TAL019416025803400                                      ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    analyzer = AdvancedA31559Analyzer()
    
    # Ejecutar múltiples estrategias de análisis
    print("🔍 Analizando endpoints directos de archivos...")
    analyzer.try_direct_file_endpoints()
    
    print("\n🔍 Analizando API con diferentes formatos...")
    analyzer.try_api_with_different_formats()
    
    print("\n🔍 Analizando sitemaps y archivos de descubrimiento...")
    analyzer.try_sitemap_discovery()
    
    print("\n🔍 Probando estructuras JSON alternativas...")
    analyzer.try_json_with_different_structure()
    
    # Analizar y guardar resultados
    analyzer.analyze_results()
    results_file = analyzer.save_results()
    
    print(f"\n✅ Análisis completado exitosamente.")
    print(f"📁 Archivo de resultados: {results_file}")

if __name__ == "__main__":
    main()