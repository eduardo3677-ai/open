#!/usr/bin/env python3
"""
Analizador Ejecutable de Acer - Script para descargar imágenes de recuperación
Basado en análisis de lógica de descarga encontrada en ejecutables de Acer
"""

import requests
import json
import hashlib
import re
from typing import Dict, Optional, Tuple, List
from urllib.parse import urlparse, parse_qs
import time
import os

class AcerImageDownloader:
    """Descargador de imágenes de recuperación de Acer basado en análisis ejecutables"""
    
    # API endpoints descubiertos
    BASE_URL = "https://device-info-prd-imub2p4wyq-uc.a.run.app"
    FALLBACK_URL = "https://device-info-uat-ycrmvsk7ia-uc.a.run.app"
    
    # Headers HTTP descubiertos desde análisis binario
    DEFAULT_HEADERS = {
        "User-Agent": "AcerDIAgent/1.0",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)
        self.device_info = None
        
    def get_api_endpoints(self) -> List[str]:
        """Obtener lista de endpoints API descubiertos"""
        return [
            self.BASE_URL,
            self.FALLBACK_URL,
            "https://api-smartquery-int.acer.com",
            "https://api-az.cdp.acer.com"
        ]
    
    def extract_device_model_from_snid(self, snid: str) -> Optional[str]:
        """Extrae modelo desde SNID basado en patrones Acer"""
        # Patrones SNID típicos de Acer
        patterns = [
            r'A315-\d{2}',  # Aspire A315 series
            r'A\d{4,5}',     # Aspire modern models
            r'Nitro \d+',    # Nitro series
            r'Predator \d+', # Predator series
            r'Swift \d+'     # Swift series
        ]
        
        for pattern in patterns:
            match = re.search(pattern, snid, re.IGNORECASE)
            if match:
                return match.group()
                
        return None
    
    def build_device_payload(self, device_model: str, snid: Optional[str] = None) -> Dict:
        """Construye payload de solicitud basado en estructura encontrada"""
        payload = {
            "model": device_model.upper(),
            "request_type": "factory_image",
            "os_version": "Windows 11",
            "format": "full_recovery"
        }
        
        if snid:
            payload["snid"] = snid.strip()
            payload["serial_number"] = snid.strip()
            
        return payload
    
    def query_device_info(self, device_model: str, snid: Optional[str] = None) -> Dict:
        """Consulta API de información de dispositivo"""
        print(f"Consultando API para: {device_model}")
        
        payload = self.build_device_payload(device_model, snid)
        
        # Intentar con diferentes métodos de solicitud
        methods = ['GET', 'POST']
        content_types = ['application/json', 'application/x-www-form-urlencoded']
        
        for base_url in [self.BASE_URL, self.FALLBACK_URL]:
            for method in methods:
                for content_type in content_types:
                    headers = self.DEFAULT_HEADERS.copy()
                    headers["Content-Type"] = content_type
                    
                    try:
                        if method == 'GET':
                            response = self.session.get(
                                base_url,
                                params=payload if content_type == 'application/x-www-form-urlencoded' else None,
                                headers=headers,
                                timeout=30
                            )
                        else:
                            if content_type == 'application/json':
                                response = self.session.post(base_url, json=payload, headers=headers, timeout=30)
                            else:
                                response = self.session.post(base_url, data=payload, headers=headers, timeout=30)
                            
                        if response.status_code == 200:
                            try:
                                data = response.json()
                                print(f"Respuesta exitosa desde {base_url}")
                                return data
                            except:
                                pass
                                
                    except Exception as e:
                        continue
        
        # Intentar endpoints adicionales descubiertos
        additional_endpoints = [
            "https://api-smartquery-int.acer.com/device/info",
            "https://api-az.cdp.acer.com/company/devices",
            "https://download.acer.com/api/v1/factory_image"
        ]
        
        for endpoint in additional_endpoints:
            try:
                response = self.session.get(endpoint, params=payload, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    print(f"Respuesta exitosa desde {endpoint}")
                    return data
            except Exception:
                continue
                
        return {"error": "Unable to query device information"}
    
    def parse_download_url(self, response_data: Dict) -> Optional[str]:
        """Parsea respuesta para encontrar URL de descarga"""
        # Patrones comunes descubiertos en análisis binario
        possible_fields = [
            'download_url', 'downloadUrl', 'download_location',
            'recovery_image_url', 'image_url', 'url',
            'factory_image', 'recovery_image',
            'download_link', 'file_url',
            'media_url', 'content_url'
        ]
        
        response_str = json.dumps(response_data)
        
        # Buscar URLs directas
        url_pattern = re.compile(r'https?://[^\s<>"{}|\\^`[\]]+')
        urls = url_pattern.findall(response_str)
        
        for url in urls:
            # Filtrar URLs que parecen de descarga de imágenes
            if any(keyword in url.lower() for keyword in ['download', 'image', 'recovery', 'factory', 'iso', 'zip']):
                return url
                
        for field in possible_fields:
            if field in response_data:
                return response_data[field]
                
        return None
    
    def get_download_authentication(self, url: str) -> Optional[Dict]:
        """Intenta obtener autenticación de descarga basada en headers encontrados"""
        try:
            response = self.session.head(url, timeout=30)
            
            if response.status_code == 200:
                auth_headers = {}
                
                for header in ['Authorization', 'X-Auth-Token', 'X-Access-Token']:
                    if header in response.headers:
                        auth_headers[header] = response.headers[header]
                        
                # Buscar cookies específicas
                auth_cookies = {}
                for cookie in response.cookies:
                    if any(keyword in cookie.name.lower() for keyword in ['auth', 'token', 'session']):
                        auth_cookies[cookie.name] = cookie.value
                        
                return {
                    'headers': auth_headers,
                    'cookies': auth_cookies,
                    'content_type': response.headers.get('Content-Type', ''),
                    'content_length': response.headers.get('Content-Length', '0')
                }
                
        except Exception as e:
            print(f"Error obteniendo autenticación: {e}")
            
        return None
    
    def download_factory_image(self, device_model: str, snid: Optional[str] = None, 
                               save_path: str = "./") -> Tuple[bool, Optional[str]]:
        """Descarga imagen de recuperación para el dispositivo"""
        print(f"\n{'='*60}")
        print(f"Descarga de Imagen de Recuperación Acer")
        print(f"{'='*60}")
        print(f"Modelo: {device_model}")
        if snid:
            print(f"SNID: {snid}")
        print(f"{'='*60}\n")
        
        # Consultar información del dispositivo
        self.device_info = self.query_device_info(device_model, snid)
        
        if "error" in self.device_info:
            print(f"Error al consultar dispositivo: {self.device_info["error"]}")
            return False, None
            
        print("Respuesta del servidor:")
        print(json.dumps(self.device_info, indent=2))
        
        # Obtener URL de descarga
        download_url = self.parse_download_url(self.device_info)
        
        if not download_url:
            print("No se encontró URL de descarga en la respuesta")
            return False, None
            
        print(f"\nURL de descarga encontrada: {download_url}")
        
        # Obtener autenticación
        auth_info = self.get_download_authentication(download_url)
        if auth_info:
            print(f"Content-Type: {auth_info['content_type']}")
            print(f"Content-Length: {auth_info['content_length']} bytes")
            
            if auth_info['headers']:
                print(f"Headers de autenticación: {auth_info['headers']}")
            if auth_info['cookies']:
                print(f"Cookies de autenticación: {auth_info['cookies']}")
        
        # Descargar archivo
        try:
            print("\nIniciando descarga...")
            response = self.session.get(
                download_url,
                stream=True,
                timeout=60,
                headers=auth_info.get('headers', {}) if auth_info else {}
            )
            response.raise_for_status()
            
            filename = download_url.split("/")[-1] or f"{device_model.replace(' ', '_')}_recovery.zip"
            filepath = os.path.join(save_path, filename)
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        
                        if total_size > 0:
                            progress = (downloaded_size / total_size) * 100
                            print(f"\rProgreso: {progress:.1f}% ({downloaded_size}/{total_size} bytes)", end='')
            
            print(f"\n\nDescarga completada: {filepath}")
            
            # Verificar integridad del archivo
            file_size = os.path.getsize(filepath)
            print(f"Tamaño del archivo descargado: {file_size} bytes")
            
            if total_size > 0 and file_size == total_size:
                print("✓ Verificación de tamaño: Exitoso")
            else:
                print("⚠ Verificación de tamaño: Aviso de discrepancia")
                
            return True, filepath
            
        except Exception as e:
            print(f"\nError en la descarga: {e}")
            return False, None
    
    def analyze_download_headers(self, url: str) -> Dict:
        """Analiza headers HTTP para comprender formato de solicitud"""
        try:
            # Intentar diferentes métodos de solicitud
            methods_data = {}
            
            for method in ['HEAD', 'GET', 'OPTIONS']:
                try:
                    response = self.session.request(method, url, timeout=30)
                    methods_data[method] = {
                        'status_code': response.status_code,
                        'headers': dict(response.headers),
                        'content_type': response.headers.get('Content-Type', ''),
                        'content_length': response.headers.get('Content-Length', '0')
                    }
                except Exception:
                    continue
                    
            return methods_data
            
        except Exception as e:
            return {"error": str(e)}
    
    def extract_form_parameters(self, url: str) -> List[str]:
        """Extrae parámetros de formulario típicos usados en endpoints de Acer"""
        common_params = [
            'model', 'snid', 'serial_number', 'os_version',
            'request_type', 'format', 'language', 'region',
            'device_type', 'manufacturer', 'bios_version',
            'download_type', 'product_code', 'part_number'
        ]
        
        # Buscar en URL y respuesta
        parsed_url = urlparse(url)
        url_params = list(parse_qs(parsed_url.query).keys())
        
        return list(set(common_params + url_params))

def main():
    """Función principal de ejecución"""
    
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║  Descargador de Imágenes de Recuperación de Acer                   ║
║  Baseado en análisis de ejecutables y DLLs                         ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    # Uso básico
    if len(os.sys.argv) >= 2:
        device_model = " ".join(os.sys.argv[1:])
        snid = None
        
        # Buscar SNID en argumentos
        if '--snid' in os.sys.argv:
            snid_index = os.sys.argv.index('--snid')
            if snid_index + 1 < len(os.sys.argv):
                snid = os.sys.argv[snid_index + 1]
                device_model = device_model.replace(f"--snid {snid}", "").strip()
        
        downloader = AcerImageDownloader()
        success, filepath = downloader.download_factory_image(device_model, snid)
        
        if success:
            print(f"\n✓ Descarga exitosa: {filepath}")
        else:
            print(f"\n✗ Descarga fallida")
            
    else:
        print("Uso:")
        print("python download_acer_images.py <modelo_del_dispositivo> [--snid <snid>]")
        print("\nEjemplos:")
        print("python download_acer_images.py ASPIRE A315-59")
        print("python download_acer_images.py ASPIRE A315-59 --snid ABC123456789")
        print("\nModelos de Acer comunes:")
        print("- ASPIRE A315-59")
        print("- ASPIRE A515-56")
        print("- NITRO 5")
        print("- PREDATOR HELIOS 300")
        print("- SWIFT 3")

if __name__ == "__main__":
    main()