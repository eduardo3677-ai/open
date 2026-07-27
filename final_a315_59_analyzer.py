#!/usr/bin/env python3
"""
Script final de análisis para archivos de recuperación del A315-59
Intenta descubrir patrones específicos de Acer para archivos de recuperación
"""

import requests
import json
import re
import os
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from typing import Dict, List, Optional

class FinalA31559Analyzer:
    """Analizador final para descubrir archivos de recuperación del A315-59"""
    
    SNID = "NXK6TAL019416025803400"
    MODEL = "A315-59"
    
    # Patrones descubiertos en análisis de ejecutables Acer
    POSSIBLE_FILE_PATTERNS = [
        "A315-59_Rcovery",
        "A315-59_Recovery",
        "A315-59_Factory",
        "A315-59_System",
        "A315-59_Image",
        "A315-59_Windows",
        "A315-59_Win11",
        "A315-59_Windows11",
        "A315-59_ISO",
        "A315-59_Zip",
        "A315-59_Rar",
        "ASPIRE_A315-59_Recovery",
        "ASPIRE_A315-59_Factory",
        "A31559_Recovery",
        "A31559_Factory",
        "NXK6TAL019416025803400_Recovery",
        f"{SNID}_Recovery",
        "Acer_A315-59_Recovery",
        "Acer_A315-59_Factory"
    ]
    
    POSSIBLE_DOMAINS = [
        "download.acer.com",
        "support.acer.com",
        "gd.acer.com",
        "files.acer.com", 
        "drivers.partners.extranet.acer.com",
        "download1.acer.com",
        "download2.acer.com",
        "cdn.acer.com",
        "storage.acer.com"
    ]
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "AcerDIAgent/1.0",
            "Accept": "*/*"
        })
        self.discovered_files = []
        
    def try_sitemap_content_discovery(self):
        """Intenta descubrir archivos a través de sitemaps"""
        sitemap_urls = [
            "https://www.acer.com/sitemap.xml",
            "https://support.acer.com/sitemap.xml",
            "https://gd.acer.com/sitemap.xml"
        ]
        
        print("🔍 Analizando sitemaps para descubrir archivos...")
        
        for sitemap in sitemap_urls:
            try:
                response = self.session.get(sitemap, timeout=15)
                
                if response.status_code == 200:
                    print(f"✓ Sitemap encontrado: {sitemap}")
                    
                    # Analizar el contenido del sitemap
                    soup = BeautifulSoup(response.text, 'xml')
                    url_elements = soup.find_all('url')
                    
                    for url_element in url_elements:
                        loc = url_element.find('loc')
                        if loc:
                            url = loc.text
                            
                            # Buscar URLs que parezcan archivos de recuperación
                            if any(pattern in url for pattern in ["A315-59", "Recovery", "Factory", "Image"]):
                                if any(ext in url for ext in [".zip", ".iso", ".exe", ".rar", ".7z"]):
                                    file_info = {
                                        "url": url,
                                        "source": "sitemap",
                                        "pattern": "recovery/ISO/ZIP file"
                                    }
                                    self.discovered_files.append(file_info)
                                    print(f"  📁 Archivo potencial: {url}")
                                    
            except Exception as e:
                continue
                
    def try_robots_txt_analysis(self):
        """Analiza archivos robots.txt buscando patrones"""
        robots_urls = [
            "https://www.acer.com/robots.txt",
            "https://support.acer.com/robots.txt",
            "https://download.acer.com/robots.txt"
        ]
        
        print("\n🔍 Analizando archivos robots.txt...")
        
        for robots_url in robots_urls:
            try:
                response = self.session.get(robots_url, timeout=10)
                
                if response.status_code == 200:
                    print(f"✓ Robots.txt encontrado: {robots_url}")
                    content = response.text
                    
                    # Buscar sitemaps y patrones en robots.txt
                    sitemap_matches = re.findall(r'Sitemap:\s*(.+)', content, re.IGNORECASE)
                    for sitemap in sitemap_matches:
                        file_info = {
                            "url": sitemap.strip(),
                            "source": "robots.txt",
                            "pattern": "sitemap discovered"
                        }
                        self.discovered_files.append(file_info)
                        
                        # Intentar acceder al sitemap descubierto
                        try:
                            sitemap_response = self.session.get(sitemap.strip(), timeout=15)
                            if sitemap_response.status_code == 200:
                                print(f"  📄 Sitemap accesible: {sitemap.strip()}")
                        except:
                            pass
                            
            except Exception as e:
                continue
                
    def try_url_patterns_from_analysis(self):
        """Prueba patrones de URL basados en el análisis de ejecutables"""
        print("\n🔍 Probando patrones de URL de ejemplos de recovery...")
        
        # Patrones basados en análisis de ejemplos de recovery
        patterns = [
            f"https://gd.acer.com/Drivers/CID/{self.MODEL}",
            f"https://gd.acer.com/Drivers/CID/09/{self.MODEL}",
            f"https://gd.acer.com/Drivers/CID/NI/{self.MODEL}",
            f"https://support.acer.com/Drivers/CID/{self.MODEL}",
            f"https://support.acer.com/Drivers/CID/NI/{self.MODEL}",
            f"https://download.acer.com/Drivers/CID/{self.MODEL}",
        ]
        
        for pattern in patterns:
            try:
                response = self.session.get(pattern, timeout=10)
                
                if response.status_code != 404:
                    print(f"✓ Patrón funcional: {pattern} - Status: {response.status_code}")
                    
                    file_info = {
                        "url": pattern,
                        "source": "gd pattern",
                        "status_code": response.status_code
                    }
                    self.discovered_files.append(file_info)
                    
                    # Analizar el contenido buscando archivos
                    if response.status_code == 200:
                        content = response.text
                        
                        # Buscar enlaces a archivos
                        soup = BeautifulSoup(content, 'html.parser')
                        links = soup.find_all('a', href=True)
                        
                        for link in links:
                            href = link['href']
                            if any(ext in href for ext in [".zip", ".iso", ".exe", ".rar", ".7z"]):
                                full_url = urljoin(pattern, href)
                                file_info = {
                                    "url": full_url,
                                    "source": "gd page analysis",
                                    "pattern": "download link"
                                }
                                self.discovered_files.append(file_info)
                                print(f"  📁 Enlace de descarga: {full_url}")
                                
            except Exception as e:
                continue
                
    def try_aspire_specific_patterns(self):
        """Estrategias específicas para la serie Aspire"""
        print("\n🔍 Probando patrones específicos de Aspire...")
        
        # Patrones específicos de la serie Aspire
        aspire_patterns = [
            f"https://gd.acer.com/Service/{self.MODEL}/Download",
            f"https://gd.acer.com/Download/Drivers/{self.MODEL}",
            f"https://support.acer.com/Drivers/CID/{self.MODEL}",
            f"https://service.acer.com/Drivers/CID/{self.MODEL}",
            f"https://gd.acer.com/warranty/{self.MODEL}",
            f"https://support.acer.com/drivers/{self.MODEL}",
        ]
        
        for pattern in aspire_patterns:
            try:
                response = self.session.get(pattern, timeout=15)
                
                if response.status_code != 404:
                    print(f"✓ Pattern Aspire funcional: {pattern} - Status: {response.status_code}")
                    
                    file_info = {
                        "url": pattern,
                        "source": "aspire pattern",
                        "status_code": response.status_code
                    }
                    self.discovered_files.append(file_info)
                    
                    # Analizar redirecciones
                    if response.status_code in [301, 302, 303, 307, 308]:
                        redirect_url = response.headers.get('Location', '')
                        if redirect_url:
                            file_info['redirect'] = redirect_url
                            print(f"  🔀 Redirección a: {redirect_url}")
                            
            except Exception as e:
                continue
                
    def try_file_extension_variations(self):
        """Intenta diferentes extensiones de archivo"""
        print("\n🔍 Probando variaciones de extensiones de archivo...")
        
        # Crear diferentes combinaciones de extensiones
        extensions = [".zip", ".iso", ".exe", ".rar", ".7z", ".img", ".wim", ".gz"]
        
        base_paths = [
            f"https://download.acer.com/{self.MODEL}/Recovery",
            f"https://download.acer.com/{self.MODEL}/Factory",
            f"https://gd.acer.com/{self.MODEL}/Recovery",
            f"https://gd.acer.com/{self.MODEL}/Factory",
        ]
        
        for base_path in base_paths:
            for extension in extensions:
                file_url = f"{base_path}{extension}"
                
                try:
                    response = self.session.head(file_url, timeout=10)
                    
                    if response.status_code != 404:
                        print(f"✓ Archivo encontrado: {file_url} - Status: {response.status_code}")
                        
                        file_info = {
                            "url": file_url,
                            "source": "extension variation",
                            "status_code": response.status_code,
                            "content_type": response.headers.get('Content-Type', ''),
                            "content_length": response.headers.get('Content-Length', '0')
                        }
                        self.discovered_files.append(file_info)
                        
                except Exception as e:
                    continue
                    
    def try_model_code_variations(self):
        """Intenta variaciones del código de modelo"""
        print("\n🔍 Probando variaciones del código de modelo...")
        
        # Variaciones posibles del modelo
        model_variations = [
            "A315-59", "A31559", "A315_59", "A315-59-XXXX", 
            "Aspire-A315-59", "Aspire_A315_59", "AspireA31559",
            "ASPIRE-A315-59", "ASPIRE_A315_59", "ASPIREA31559",
            f"NXK6TAL{self.SNID[-20:]}", self.SNID  # Variaciones con SNID
        ]
        
        base_urls = [
            "https://download.acer.com",
            "https://gd.acer.com",
            "https://support.acer.com"
        ]
        
        for base_url in base_urls:
            for model_var in model_variations:
                test_url = f"{base_url}/{model_var}/"
                
                try:
                    response = self.session.get(test_url, timeout=10)
                    
                    if response.status_code != 404:
                        print(f"✓ Variación funcional: {test_url} - Status: {response.status_code}")
                        
                        file_info = {
                            "url": test_url,
                            "source": "model variation",
                            "status_code": response.status_code,
                            "model_variation": model_var
                        }
                        self.discovered_files.append(file_info)
                        
                except Exception as e:
                    continue
                    
    def analyze_discovered_files(self):
        """Analiza los archivos descubiertos"""
        print(f"\n📊 ANÁLISIS DE ARCHIVOS DESUBIERTOS:")
        print(f"Total de archivos encontrados: {len(self.discovered_files)}")
        
        # Agrupar por fuente
        by_source = {}
        for file_info in self.discovered_files:
            source = file_info.get('source', 'unknown')
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(file_info)
            
        for source, files in by_source.items():
            print(f"\n🔍 Fuente: {source} ({len(files)} archivos)")
            for i, file_info in enumerate(files, 1):
                print(f"  {i}. {file_info.get('url', 'Unknown URL')}")
                if 'status_code' in file_info:
                    print(f"     Status: {file_info['status_code']}")
                if 'pattern' in file_info:
                    print(f"     Pattern: {file_info['pattern']}")
                    
    def save_final_report(self):
        """Guarda el reporte final de análisis"""
        report_file = f"a315_59_final_analysis_{int(time.time())}.json"
        
        report = {
            "device": {
                "model": self.MODEL,
                "snid": self.SNID
            },
            "analysis_summary": {
                "total_discovered_files": len(self.discovered_files),
                "analysis_methods_used": [
                    "sitemap_content_discovery",
                    "robots_txt_analysis", 
                    "url_patterns_from_analysis",
                    "aspire_specific_patterns",
                    "file_extension_variations",
                    "model_code_variations"
                ]
            },
            "discovered_files": self.discovered_files
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"\n💾 Reporte final guardado en: {report_file}")
        return report_file

def main():
    """Función principal de ejecución"""
    
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║  Análisis Final: Archivos de Recuperación A315-59                  ║
║  SNID: NXK6TAL019416025803400                                      ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    analyzer = FinalA31559Analyzer()
    
    # Ejecutar todas las estrategias de análisis
    analyzer.try_sitemap_content_discovery()
    analyzer.try_robots_txt_analysis()
    analyzer.try_url_patterns_from_analysis()
    analyzer.try_aspire_specific_patterns()
    analyzer.try_file_extension_variations()
    analyzer.try_model_code_variations()
    
    # Analizar y guardar resultados
    analyzer.analyze_discovered_files()
    report_file = analyzer.save_final_report()
    
    print(f"\n✅ Análisis final completado.")
    print(f"📁 Reporte final: {report_file}")
    print(f"📊 Total de archivos descubiertos: {len(analyzer.discovered_files)}")

if __name__ == "__main__":
    main()