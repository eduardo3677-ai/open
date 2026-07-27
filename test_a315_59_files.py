#!/usr/bin/env python3
"""
Script de prueba específico para descargar archivos del A315-59
Prueba las URLs descubiertas para encontrar archivos de recuperación reales
"""

import requests
import json
import os
import re
from bs4 import BeautifulSoup
from typing import Dict, List, Optional

class A31559FileTester:
    """Tester específico para archivos del A315-59"""
    
    SNID = "NXK6TAL019416025803400"
    MODEL = "A315-59"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "AcerDIAgent/1.0",
            "Accept": "*/*"
        })
        self.recovery_files = []
        
    def test_discovered_urls(self):
        """Prueba las URLs descubiertas en el análisis"""
        
        # URLs descubiertas que funcionaron
        urls_to_test = [
            "https://support.acer.com/Drivers/CID/A315-59",
            "https://support.acer.com/Drivers/CID/NI/A315-59",
            "https://support.acer.com/drivers/A315-59",
            "https://support.acer.com/A315-59/",
            "https://support.acer.com/NXK6TAL019416025803400/",
        ]
        
        print("🔍 Probando URLs descubiertas para archivos de recuperación...")
        
        for url in urls_to_test:
            print(f"\n📄 Analizando: {url}")
            
            try:
                response = self.session.get(url, timeout=15)
                
                if response.status_code == 200:
                    self.analyze_page_content(url, response.text)
                    
            except Exception as e:
                print(f"✗ Error analizando {url}: {e}")
                
    def analyze_page_content(self, base_url, html_content):
        """Analiza el contenido de la página buscando archivos"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Buscar todos los enlaces
        links = soup.find_all('a', href=True)
        
        print(f"  📋 Total de enlaces encontrados: {len(links)}")
        
        for link in links:
            href = link['href']
            text = link.get_text(strip=True)
            
            # Construir URL completa
            full_url = requests.compat.urljoin(base_url, href)
            
            # Buscar patrones de archivos de recuperación
            is_recovery_file = self.check_recovery_patterns(full_url, text)
            
            if is_recovery_file:
                print(f"  🎯 ARCHIVO DE RECUPERACIÓN POTENCIAL: {full_url}")
                print(f"     Texto: {text}")
                
                # Obtener más información del archivo
                file_info = self.get_file_info(full_url)
                
                # Probar descarga del archivo
                test_download = self.test_file_download(full_url)
                
                recovery_file = {
                    "url": full_url,
                    "text": text,
                    "file_info": file_info,
                    "download_test": test_download
                }
                
                self.recovery_files.append(recovery_file)
                
    def check_recovery_patterns(self, url, text):
        """Verifica si el enlace corresponde a un archivo de recuperación"""
        recovery_keywords = [
            "recovery", "Recovery", "RECOVERY",
            "factory", "Factory", "FACTORY", 
            "image", "Image", "IMAGE",
            "system", "System", "SYSTEM",
            "restore", "Restore", "RESTORE",
            "backup", "Backup", "BACKUP",
            "reset", "Reset", "RESET",
            "windows", "Windows", "WINDOWS",
            "iso", "ISO",
            "zip", "ZIP",
            "download", "Download", "DOWNLOAD"
        ]
        
        # Verificar extensión del archivo
        if any(ext in url.lower() for ext in [".iso", ".zip", ".exe", ".rar", ".7z", ".img", ".wim", ".gz"]):
            # Si tiene extensión de archivo, buscar palabras clave
            if any(keyword in url.lower() or keyword in text.lower() for keyword in recovery_keywords):
                return True
                
        # Verificar palabras clave específicas de recuperación
        if any(keyword in text.lower() for keyword in [
            "recovery image", "factory image", "system image", 
            "reset pc", "reset this pc", "installation media",
            "boot media", "bootable usb", "recovery disk",
            "factory reset", "system restore"
        ]):
            return True
            
        # Verificar si contiene código de modelo en la URL
        if self.MODEL in url or "A315-59" in url:
            if any(ext in url.lower() for ext in [".iso", ".zip", ".exe"]):
                return True
                
        return False
        
    def get_file_info(self, url):
        """Obtiene información del archivo"""
        file_info = {}
        
        try:
            response = self.session.head(url, timeout=10, allow_redirects=True)
            
            file_info = {
                "status_code": response.status_code,
                "content_type": response.headers.get('Content-Type', ''),
                "content_length": response.headers.get('Content-Length', '0'),
                "last_modified": response.headers.get('Last-Modified', ''),
                "location": response.headers.get('Location', url),
                "headers": dict(response.headers)
            }
            
            # Intentar obtener el nombre del archivo
            filename = url.split('/')[-1]
            if filename:
                file_info['filename'] = filename
                
        except Exception as e:
            file_info['error'] = str(e)
            
        return file_info
        
    def test_file_download(self, url):
        """Prueba la descarga del archivo (solo los primeros bytes)"""
        download_info = {}
        
        try:
            # Solo descargar los primeros 1024 bytes para probar
            response = self.session.get(url, timeout=15, stream=True)
            
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                content_length = response.headers.get('Content-Length', '0')
                
                download_info = {
                    "status_code": response.status_code,
                    "content_type": content_type,
                    "content_length": content_length,
                    "downloadable": True
                }
                
                # Leer los primeros bytes para verificar tipo de archivo
                first_bytes = next(response.iter_content(1024))
                download_info['file_signature'] = first_bytes[:20].hex()
                
                # Verificar si es un archivo ZIP, ISO u otro tipo
                if content_type == 'application/zip' or first_bytes.startswith(b'PK'):
                    download_info['file_type'] = 'ZIP archive'
                elif content_type == 'application/octet-stream' or first_bytes.startswith(b'PK'):
                    download_info['file_type'] = 'Possible ZIP archive'
                elif content_type == 'application/x-iso9660-image':
                    download_info['file_type'] = 'ISO image'
                elif content_type == 'application/x-msdownload' or first_bytes.startswith(b'MZ'):
                    download_info['file_type'] = 'Windows executable'
                else:
                    download_info['file_type'] = 'Unknown'
                    
            else:
                download_info = {
                    "status_code": response.status_code,
                    "downloadable": False
                }
                
        except Exception as e:
            download_info = {
                "error": str(e),
                "downloadable": False
            }
            
        return download_info
        
    def search_specific_recovery_paths(self):
        """Busca rutas específicas para archivos de recuperación"""
        print("\n🔍 Buscando rutas específicas de recuperación...")
        
        # Rutas específicas basadas en patterns de Acer
        specific_paths = [
            f"https://support.acer.com/Drivers/CID/{self.MODEL}/Recovery",
            f"https://support.acer.com/Drivers/CID/NI/{self.MODEL}/Recovery",
            f"https://support.acer.com/drivers/{self.MODEL}/recovery",
            f"https://support.acer.com/drivers/{self.MODEL}/factory",
            f"https://gd.acer.com/Drivers/CID/{self.MODEL}/Recovery",
            f"https://gd.acer.com/Service/{self.MODEL}/Factory",
        ]
        
        for path in specific_paths:
            try:
                response = self.session.get(path, timeout=10)
                
                if response.status_code != 404:
                    print(f"✓ Ruta específica encontrada: {path} - Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        self.analyze_page_content(path, response.text)
                        
            except Exception as e:
                continue
                
    def test_snid_specific_endpoints(self):
        """Prueba endpoints específicos para el SNID"""
        print(f"\n🔍 Probando endpoints específicos para SNID: {self.SNID}")
        
        # Endpoints específicos para SNID
        snid_endpoints = [
            f"https://support.acer.com/api/Recovery/{self.SNID}",
            f"https://support.acer.com/api/Factory/{self.SNID}",
            f"https://gd.acer.com/api/Recovery/{self.SNID}",
            f"https://download.acer.com/api/Recovery/{self.SNID}",
            f"https://support.acer.com/Recovery/{self.SNID}",
        ]
        
        for endpoint in snid_endpoints:
            try:
                response = self.session.get(endpoint, timeout=10)
                
                if response.status_code != 404:
                    print(f"✓ Endpoint SNID funcional: {endpoint} - Status: {response.status_code}")
                    
                    # Si es respuesta JSON, analizar
                    try:
                        json_data = response.json()
                        print(f"  📄 JSON Response:")
                        print(f"     {json.dumps(json_data, indent=2)[:500]}")
                        
                        # Buscar URLs de descarga en el JSON
                        json_str = json.dumps(json_data)
                        urls = re.findall(r'https?://[^\s<>"{}|\\^`[\]]+', json_str)
                        
                        for url in urls:
                            if any(keyword in url.lower() for keyword in ['download', 'file', 'recovery']):
                                print(f"  🎯 URL encontrada en JSON: {url}")
                                
                    except:
                        # Si no es JSON, analizar como HTML
                        if response.status_code == 200:
                            self.analyze_page_content(endpoint, response.text)
                            
            except Exception as e:
                continue
                
    def analyze_results(self):
        """Analiza los resultados de las pruebas"""
        print(f"\n📊 ANÁLISIS DE RESULTADOS:")
        print(f"Total de archivos de recuperación encontrados: {len(self.recovery_files)}")
        
        if self.recovery_files:
            print(f"\n🎯 ARCHIVOS DE RECUPERACIÓN DETECTADOS:")
            for i, file_info in enumerate(self.recovery_files, 1):
                print(f"\n{i}. {file_info['url']}")
                print(f"   Texto del enlace: {file_info['text']}")
                print(f"   Tipo de archivo: {file_info.get('file_info', {}).get('Content-Type', '')}")
                print(f"   Tamaño: {file_info.get('file_info', {}).get('Content-Length', '0')} bytes")
                
                download_test = file_info.get('download_test', {})
                if download_test.get('downloadable'):
                    print(f"   ✅ Descargable: SÍ")
                    if 'file_type' in download_test:
                        print(f"   📦 Tipo: {download_test['file_type']}")
                else:
                    print(f"   ❌ Descargable: NO")
                    
    def save_results(self):
        """Guarda los resultados en un archivo JSON"""
        results_file = f"a315_59_recovery_files_{int(time.time())}.json"
        
        results = {
            "device": {
                "model": self.MODEL,
                "snid": self.SNID
            },
            "total_recovery_files_found": len(self.recovery_files),
            "recovery_files": self.recovery_files
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
        print(f"\n💾 Resultados guardados en: {results_file}")
        return results_file

def main():
    """Función principal de ejecución"""
    
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║  Buscador de Archivos de Recuperación A315-59                      ║
║  SNID: NXK6TAL019416025803400                                      ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    tester = A31559FileTester()
    
    # Ejecutar todas las pruebas
    tester.test_discovered_urls()
    tester.search_specific_recovery_paths()
    tester.test_snid_specific_endpoints()
    
    # Analizar y guardar resultados
    tester.analyze_results()
    results_file = tester.save_results()
    
    print(f"\n✅ Pruebas completadas.")
    print(f"📁 Resultados guardados en: {results_file}")
    print(f"📊 Archivos de recuperación encontrados: {len(tester.recovery_files)}")

if __name__ == "__main__":
    import time
    main()