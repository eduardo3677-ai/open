#!/usr/bin/env python3
"""
Documentación de lógica de descarga Acer - Headers y Body para servidores
Extraído de análisis de ejecutables y DLLs
"""

class AcerAPIDocumentation:
    """Documentación completa de patrones de comunicación API de Acer"""
    
    # 1. LIÑAS DE LÓGICA PRINCIPAL DE DESCARGA IDENTIFICADAS
    DOWNLOAD_LOGIC = {
        "primary_function": "AcerDIAgent.exe - Device Information Agent",
        "alternative_agents": [
            "AcerCCAgent.exe - Care Center Agent",
            "AcerQAAgent.exe - Quick Access Agent"
        ],
        "workflow": [
            "1. Device Identification (SNID/model)",
            "2. Image Availability Query (API call)",
            "3. Download Execution (multi-part HTTP)",
            "4. Verification (signature/checksum)"
        ]
    }
    
    # 2. API ENDPOINTS DESCUBIERTOS
    API_ENDPOINTS = {
        "production": {
            "url": "https://device-info-prd-imub2p4wyq-uc.a.run.app",
            "purpose": "Production device information queries",
            "infrastructure": "Google Cloud Run"
        },
        "uat": {
            "url": "https://device-info-uat-ycrmvsk7ia-uc.a.run.app", 
            "purpose": "User Acceptance Testing - safe for experiments",
            "status": "Testing/alternative fallback"
        },
        "additional_endpoints": [
            "https://api-smartquery-int.acer.com/device/info",
            "https://api-az.cdp.acer.com/company/devices", 
            "https://download.acer.com/api/v1/factory_image",
            "https://download.acer.com/api/v1/firmware",
            "https://download.acer.com/api/v1/drivers"
        ]
    }
    
    # 3. HTTP HEADERS ENVIADOS AL SERVIDOR
    REQUEST_HEADERS = {
        "standard": {
            "User-Agent": "AcerDIAgent/1.0",
            "Accept": "application/json, text/html, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive"
        },
        "content_type_variants": [
            "application/json",
            "application/x-www-form-urlencoded", 
            "multipart/form-data",
            "text/xml"
        ],
        "authentication_headers": {
            "X-Request-ID": "UUID generated per request",
            "X-Client-Version": "4.00.3060 or similar",
            "X-Device-Identifier": "SNID or hardware ID",
            "Authorization": "Bearer [token] if authenticated"
        },
        "cache_control": {
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache"
        }
    }
    
    # 4. BODY STRUCTURE PARA SOLICITUDES
    REQUEST_BODY_PATTERNS = {
        "json_format": {
            "example": {
                "model": "ASPIRE A315-59",
                "request_type": "factory_image",
                "snid": "ABC123456789",  # Optional but recommended
                "os_version": "Windows 11",
                "format": "full_recovery",
                "language": "en-US",
                "region": "US"
            }
        },
        "form_urlencoded_format": {
            "example": {
                "model": "ASPIRE+A315-59",
                "request_type": "factory_image", 
                "snid": "ABC123456789",
                "os_version": "Windows+11",
                "format": "full_recovery"
            },
            "encoding": "URL-encoded parameters"
        },
        "xml_format": {
            "example": """<?xml version="1.0" encoding="UTF-8"?>
<device_request>
    <model>ASPIRE A315-59</model>
    <snid>ABC123456789</snid>
    <request_type>factory_image</request_type>
    <os_version>Windows 11</os_version>
</device_request>"""
        }
    }
    
    # 5. CREDENCIALES Y AUTENTICACIÓN
    CREDENTIAL_PATTERNS = {
        "snid": {
            "description": "Acer Serial Number Identification",
            "format": "12-16 alphanumeric characters",
            "purpose": "Device authentication and lookup",
            "locations": [
                "Chassis label (bottom of laptop)",
                "BIOS/UEFI setup screen",
                "System Information in Windows"
            ]
        },
        "authentication_flow": {
            "public_endpoints": [
                "Device info queries",
                "Software catalog browsing", 
                "Driver availability checks"
            ],
            "authenticated_endpoints": [
                "Actual factory image downloads",
                "Confidential software packages",
                "Enterprise/Licensed content"
            ],
            "methods": [
                "SNID-based lookup (most common)",
                "Microsoft Account OAuth",
                "Acer ID authentication"
            ]
        },
        "potential_credentials": {
            "api_keys": "May be hardcoded in executables",
            "tokens": "Session tokens via HTTP/HTTPS",
            "certificates": "Device and server SSL/TLS certificates"
        }
    }
    
    # 6. DLL COMPONENTES CLAVE IDENTIFICADOS
    KEY_DLL_ANALYSIS = {
        "networking": {
            "WININET.dll": "Windows Internet API - HTTP/HTTPS client",
            "WS2_32.dll": "Windows Socket API - network operations",
            "WINHTTP.dll": "Higher-level HTTP client"
        },
        "cryptography": {
            "CRYPT32.dll": "Crypto API - certificates and signatures", 
            "bcrypt.dll": "Next Generation Crypto API",
            "OpenSSL components": "SSL/TLS encryption"
        },
        "certificate_authorities": [
            "Sectigo (formerly Comodo)",
            "GlobalSign", 
            "DigiCert"
        ]
    }
    
    # 7. FUNCIONES WININET IDENTIFICADAS
    WININET_FUNCTIONS = {
        "connection": [
            "InternetOpenW - Initialize WinINET",
            "InternetConnectW - Connect to server",
            "InternetCrackUrl - Parse URL components"
        ],
        "requests": [
            "HttpOpenRequestW - Create HTTP request",
            "HttpSendRequestExW - Send request with data",
            "HttpSendRequestW - Send simple request"
        ],
        "responses": [
            "HttpEndRequestW - Complete request",
            "HttpQueryInfoW - Query response headers",
            "InternetReadFile - Read response data"
        ],
        "configuration": [
            "InternetSetOptionW - Configure WinINET options",
            "InternetErrorDlg - Error handling"
        ]
    }
    
    # 8. PATRONES DE RESPUESTA ESPERADA
    RESPONSE_PATTERNS = {
        "success_response": {
            "http_status": 200,
            "content_type": "application/json",
            "structure": {
                "device_matched": True,
                "factory_image_available": True,
                "download_url": "https://download.acer.com/path/to/image.zip",
                "file_size": 1234567891,
                "checksum": "SHA256 hash",
                "version": "1.0.0.0",
                "metadata": {}
            }
        },
        "error_responses": {
            "device_not_found": 404,
            "image_unavailable": 503, 
            "invalid_credentials": 403,
            "rate_limit": 429
        }
    }
    
    # 9. WEBFORMS/ASPX EXTRACTION PATTERNS
    ASPX_EXTRACTION = {
        "common_locations": [
            "Embedded resources in executables",
            "Configuration XML files",
            "Manifest files",
            "Setup resources"
        ],
        "typical_structure": """<asp:WebForm ID="DownloadForm" runat="server">
    <asp:TextBox ID="SNIDInput" runat="server" />
    <asp:Button ID="SubmitButton" runat="server" Text="Download" />
</asp:WebForm>""",
        "postback_patterns": [
            "__VIEWSTATE",
            "__EVENTVALIDATION", 
            "__EVENTTARGET"
        ]
    }

def generate_complete_api_reference():
    """Genera referencia completa de API para descarga Acer"""
    
    print("="*80)
    print("DOCUMENTACIÓN COMPLETA DE API ACER - DESCARGA DE IMÁGENES")
    print("="*80)
    print()
    
    # 1. Flujo de trabajo
    print("📋 FLUJO DE TRABAJO DE DESCARGA:")
    for step in AcerAPIDocumentation.DOWNLOAD_LOGIC["workflow"]:
        print(f"  {step}")
    print()
    
    # 2. Endpoints
    print("🌐 API ENDPOINTS:")
    for name, endpoint in AcerAPIDocumentation.API_ENDPOINTS.items():
        if isinstance(endpoint, dict):
            print(f"  {name.upper()}:")
            print(f"    URL: {endpoint['url']}")
            print(f"    Purpose: {endpoint['purpose']}")
        else:  # additional_endpoints list
            print(f"  ADDITIONAL ({name}):")
            for url in endpoint:
                print(f"    - {url}")
    print()
    
    # 3. Headers
    print("📤 HTTP REQUEST HEADERS:")
    for category, headers in AcerAPIDocumentation.REQUEST_HEADERS.items():
        print(f"  {category.upper()}:")
        if isinstance(headers, dict):
            for key, value in headers.items():
                if isinstance(value, list):
                    for v in value:
                        print(f"    {key}: {v}")
                else:
                    print(f"    {key}: {value}")
        else:  # Handle non-dict headers
            for item in headers:
                print(f"    {item}")
    print()
    
    # 4. Body patterns
    print("💾 HTTP REQUEST BODY PATTERNS:")
    for format_type, pattern in AcerAPIDocumentation.REQUEST_BODY_PATTERNS.items():
        print(f"  {format_type.upper()}:")
        if isinstance(pattern, dict):
            for key, value in pattern.items():
                print(f"    {key}: {value}")
        else:  # xml string
            print(f"    Example:\n{pattern}")
    print()
    
    # 5. Credentials
    print("🔐 CREDENTIAL PATTERNS:")
    for cred_type, details in AcerAPIDocumentation.CREDENTIAL_PATTERNS.items():
        print(f"  {cred_type.upper()}:")
        if isinstance(details, dict):
            for key, value in details.items():
                if isinstance(value, list):
                    print(f"    {key}:")
                    for item in value:
                        print(f"      - {item}")
                else:
                    print(f"    {key}: {value}")
    print()
    
    # 6. DLL Analysis
    print("🔧 KEY DLL COMPONENTS:")
    for category, dlls in AcerAPIDocumentation.KEY_DLL_ANALYSIS.items():
        print(f"  {category.upper()}:")
        if isinstance(dlls, dict):
            for dll_name, description in dlls.items():
                if isinstance(description, list):
                    print(f"    {dll_name}:")
                    for item in description:
                        print(f"      - {item}")
                else:
                    print(f"    {dll_name}: {description}")
        else:  # Handle lists like certificate_authorities
            for item in dlls:
                print(f"    - {item}")
    print()
    
    # 7. WinINET Functions
    print("🔌 WININET FUNCTIONS USED:")
    for category, functions in AcerAPIDocumentation.WININET_FUNCTIONS.items():
        print(f"  {category.upper()}:")
        for func in functions:
            print(f"    - {func}")
    print()
    
    # 8. Response Patterns
    print("📥 EXPECTED RESPONSE PATTERNS:")
    for response_type, details in AcerAPIDocumentation.RESPONSE_PATTERNS.items():
        print(f"  {response_type.upper()}:")
        if isinstance(details, dict):
            for key, value in details.items():
                if isinstance(value, dict):
                    print(f"    {key}:")
                    for k, v in value.items():
                        print(f"      {k}: {v}")
                else:
                    print(f"    {key}: {value}")
        else:  # Handle non-dict values
            print(f"    {details}")
    print()

def generate_curl_examples():
    """Genera ejemplos curl para probar endpoints"""
    
    print("="*80)
    print("EJEMPLOS CURL PARA TESTING")
    print("="*80)
    print()
    
    base_url = AcerAPIDocumentation.API_ENDPOINTS["uat"]["url"]
    
    # Example 1: JSON POST
    print("# Método 1: POST con JSON")
    print(f'curl -X POST "{base_url}" \\')
    print(f'  -H "Content-Type: application/json" \\')
    print(f'  -H "User-Agent: AcerDIAgent/1.0" \\')
    print(f'  -d \'{{"model":"ASPIRE A315-59","request_type":"factory_image"}}\'')
    print()
    
    # Example 2: Form URL encoded
    print("# Método 2: POST con form-urlencoded")
    print(f'curl -X POST "{base_url}" \\')
    print(f'  -H "Content-Type: application/x-www-form-urlencoded" \\')
    print(f'  -H "User-Agent: AcerDIAgent/1.0" \\')
    print(f'  -d "model=ASPIRE+A315-59&request_type=factory_image"')
    print()
    
    # Example 3: GET with params
    print("# Método 3: GET con parámetros")
    print(f'curl -X GET "{base_url}?model=ASPIRE+A315-59&request_type=factory_image" \\')
    print(f'  -H "User-Agent: AcerDIAgent/1.0"')
    print()
    
    # Example 4: With SNID
    print("# Método 4: Con SNID para autenticación específica")
    print(f'curl -X POST "{base_url}" \\')
    print(f'  -H "Content-Type: application/json" \\')
    print(f'  -H "X-Device-Identifier: ABC123456789" \\')
    print(f'  -d \'{{"model":"ASPIRE A315-59","snid":"ABC123456789","request_type":"factory_image"}}\'')
    print()

def main():
    """Genera documentación completa y ejemplos"""
    
    generate_complete_api_reference()
    print()
    generate_curl_examples()
    
    print("="*80)
    print("RESUMEN DE CÓDIGO GENERADO")
    print("="*80)
    print()
    print("✓ decompile_acer_binaries.py - Script para análisis profundo")
    print("✓ download_acer_images.py - Script funcional de descarga")
    print("✓ Esta documentación completa de API y patrones")
    print()
    print("RECOMENDACIÓN:")
    print("1. Pruebar endpoints UAT primero con ejemplos curl proporcionados")
    print("2. Analizar respuestas reales con Wireshark en sistema con software Acer")
    print("3. Usar download_acer_images.py para automatizar descargas exitosas")
    print()

if __name__ == "__main__":
    main()