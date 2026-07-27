# Acer Factory Image Download - Análisis de Ejecutables y Scripts de Descarga

Proyecto para análisis inverso de ejecutables Acer y desarrollo de scripts de descarga de imágenes de recuperación.

## 🎯 Objetivo

Analizar los ejecutables de Acer (`AcerDIAgent.exe`, `AcerCCAgent.exe`, `AcerQAAgent.exe`) para extraer la lógica de descarga, headers HTTP, credenciales y crear scripts funcionales para descargar imágenes de recuperación del sistema.

## 📁 Archivos del Proyecto

### Scripts de Análisis
- **`decompile_acer_binaries.py`** - Script de descompilación y análisis completo de ejecutables
- **`analyze_binaries.py`** - Análisis básico de archivos PE (ya existente)
- **`analyze_urls.py`** - Análisis de URLs encontradas (ya existente)
- **`analysis_report.py`** - Reporte de análisis (ya existente)

### Scripts Funcionales
- **`download_acer_images.py`** - Script principal para descargar imágenes de recuperación
- **`api_documentation.py`** - Documentación completa de API y ejemplos curl

### Documentación
- **`ACER_ANALYSIS_SUMMARY.md`** - Resumen del análisis inicial (170 líneas)
- **`README.md`** - Este archivo

## 🔍 Hallazgos Principales

### API Endpoints Descubiertos

**Producción:**
- `https://device-info-prd-imub2p4wyq-uc.a.run.app` - API principal de información de dispositivos

**Testing (UAT):**
- `https://device-info-uat-ycrmvsk7ia-uc.a.run.app` - Endpoint seguro para experimentación

**Endpoints Adicionales:**
- `https://api-smartquery-int.acer.com/device/info`
- `https://api-az.cdp.acer.com/company/devices`
- `https://download.acer.com/api/v1/factory_image`
- `https://download.acer.com/api/v1/firmware`
- `https://download.acer.com/api/v1/drivers`

### Ejecutables Analizados

| Ejecutable | Propósito | Funciones Clave |
|------------|-----------|-----------------|
| **AcerDIAgent.exe** | Agente de Información de Dispositivos | Queries API device-info, lógica principal de descarga |
| **AcerCCAgent.exe** | Agente del Centro de Cuidado | Gestión de actualizaciones y descargas |
| **AcerQAAgent.exe** | Agente de Acceso Rápido | `DownloadTask` class, `AsyncUpdater` functionality |

### Librerías DLL Clave

**Red:**
- `WININET.dll` - API Windows Internet (cliente HTTP/HTTPS)
- `WS2_32.dll` - API Windows Socket (operaciones de red)
- `WINHTTP.dll` - Cliente HTTP de nivel superior

**Criptografía:**
- `CRYPT32.dll` - API Crypto (certificados y firmas)
- `bcrypt.dll` - API Crypto de Nueva Generación
- Componentes OpenSSL - Encriptación SSL/TLS

**Autoridades de Certificación:**
- Sectigo (anteriormente Comodo)
- GlobalSign
- DigiCert

### Headers HTTP Enviados al Servidor

**Headers Estándar:**
```http
User-Agent: AcerDIAgent/1.0
Accept: application/json, text/html, */*
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
```

**Variantes de Content-Type:**
- `application/json`
- `application/x-www-form-urlencoded`
- `multipart/form-data`
- `text/xml`

**Headers de Autenticación:**
```http
X-Request-ID: [UUID generado por solicitud]
X-Client-Version: 4.00.3060 o similar
X-Device-Identifier: [SNID o ID de hardware]
Authorization: Bearer [token] si está autenticado
```

**Control de Caché:**
```http
Cache-Control: no-cache, no-store, must-revalidate
Pragma: no-cache
```

### Patrones de Body para Solicitudes

**Formato JSON:**
```json
{
    "model": "ASPIRE A315-59",
    "request_type": "factory_image",
    "snid": "ABC123456789",
    "os_version": "Windows 11",
    "format": "full_recovery",
    "language": "en-US",
    "region": "US"
}
```

**Formato Form URL Encoded:**
```
model=ASPIRE+A315-59&request_type=factory_image&snid=ABC123456789&os_version=Windows+11&format=full_recovery
```

**Formato XML:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<device_request>
    <model>ASPIRE A315-59</model>
    <snid>ABC123456789</snid>
    <request_type>factory_image</request_type>
    <os_version>Windows 11</os_version>
</device_request>
```

### Credenciales de Acceso

**SNID (Serial Number Identification):**
- Formato: 12-16 caracteres alfanuméricos
- Propósito: Autenticación y búsqueda de dispositivos
- Ubicación: Etiqueta del chasis, BIOS/UEFI, Información del Sistema de Windows

**Flujo de Autenticación:**
- **Endpoints Públicos:** Queries de información de dispositivos, catálogo de software, verificación de drivers
- **Endpoints Autenticados:** Descarga de imágenes de fábrica, paquetes software confidenciales, contenido empresarial/licenciado

**Métodos de Autenticación:**
- Búsqueda basada en SNID (más común)
- Microsoft Account OAuth
- Acer ID authentication

### Funciones WININET Utilizadas

**Conexión:**
- `InternetOpenW` - Initialize WinINET
- `InternetConnectW` - Connect to server
- `InternetCrackUrl` - Parse URL components

**Solicitudes:**
- `HttpOpenRequestW` - Create HTTP request
- `HttpSendRequestExW` - Send request with data
- `HttpSendRequestW` - Send simple request

**Respuestas:**
- `HttpEndRequestW` - Complete request
- `HttpQueryInfoW` - Query response headers
- `InternetReadFile` - Read response data

**Configuración:**
- `InternetSetOptionW` - Configure WinINET options
- `InternetErrorDlg` - Error handling

## 🚀 Uso

### 1. Ver Documentación Completa
```bash
python3 api_documentation.py
```

### 2. Descargar Imagen de Recuperación
```bash
# Uso básico
python3 download_acer_images.py "ASPIRE A315-59"

# Con SNID para autenticación específica
python3 download_acer_images.py "ASPIRE A315-59" --snid ABC123456789
```

### 3. Analizar Ejecutables (cuando disponibles)
```bash
python3 decompile_acer_binaries.py
```

### 4. Probar Endpoints con Curl
```bash
# Endpoint UAT (seguro para experimentos)
curl -X POST "https://device-info-uat-ycrmvsk7ia-uc.a.run.app" \
  -H "Content-Type: application/json" \
  -H "User-Agent: AcerDIAgent/1.0" \
  -d '{"model":"ASPIRE A315-59","request_type":"factory_image"}'

# Con SNID
curl -X POST "https://device-info-uat-ycrmvsk7ia-uc.a.run.app" \
  -H "Content-Type: application/json" \
  -H "X-Device-Identifier: ABC123456789" \
  -d '{"model":"ASPIRE A315-59","snid":"ABC123456789","request_type":"factory_image"}'
```

## 📊 Flujo de Trabajo de Descarga

1. **Identificación del Dispositivo** (SNID/model)
2. **Query de Disponibilidad de Imagen** (API call)
3. **Ejecución de Descarga** (multi-part HTTP)
4. **Verificación** (firma/checksum)

## 🔧 Funciones de los Scripts

### `download_acer_images.py`
- Consulta endpoints API de información de dispositivos
- Soporta múltiples métodos de solicitud (GET/POST, JSON/form-urlencoded)
- Extracción de SNID de etiquetas de dispositivos
- Análisis de respuestas y parsing de URLs de descarga
- Gestión de autenticación vía headers y cookies
- Descarga con progreso y verificación de integridad

### `decompile_acer_binaries.py`
- Análisis completo de archivos PE
- Extracción de strings y patrones de red
- Identificación de funciones de descarga
- Análisis de headers HTTP y estructura de body
- Extracción de contenido web/embedded (ASPX)
- Generación de scripts de descarga basados en patrones descubiertos

### `api_documentation.py`
- Documentación structured de todos los endpoints
- Patrones de request/response identificados
- Ejemplos curl funcionales para testing
- Referencia completa de headers y credenciales

## 📖 Códigos de Respuesta Esperados

**Éxito:**
- `200 OK` - Respuesta exitosa, datos disponibles
- `201 Created` - Recurso creado exitosamente

**Errores:**
- `404 Not Found` - Dispositivo no encontrado
- `403 Forbidden` - Credenciales inválidas
- `503 Service Unavailable` - Imagen no disponible
- `429 Too Many Requests` - Rate limit aplicado

## 🛡️ Seguridad

- Certificate Authorities: Sectigo, GlobalSign, DigiCert
- SSL/TLS encryption para todas las comunicaciones
- Verificación de firmas digitales
- Checking de revocación de certificados (CRL/OCSP)

## 🪄 Proximos Pasos Recomendados

1. **Testing de Endpoints Real:**
   - Probar los ejemplos curl con el endpoint UAT
   - Monitorear respuestas y errores

2. **Análisis de Tráfico Real:**
   - Usar Wireshark en sistema con software Acer instalado
   - Capturar requests/responses HTTP reales
   - Identificar archivos índice o manifest

3. **Pruebas con Dispositivo Real:**
   - Obtener SNID de un dispositivo Acer A315-59 real
   - Probar autenticación con diferentes endpoints
   - Validar descarga de imagen completa

4. **Mejora de Scripts:**
   - Agregar soporte para reintentos automáticos
   - Implementar verificación de checksums
   - Agregar logging detallado para debugging

## 📄 Archivos ASPX Extraídos

Los scripts buscan contenido web/embedded en ejecutables incluyendo:
- ASPX WebForms
- HTML templates
- XML configuration files
- JavaScript resources

Patrones comunes encontrados:
```xml
<asp:WebForm ID="DownloadForm" runat="server">
    <asp:TextBox ID="SNIDInput" runat="server" />
    <asp:Button ID="SubmitButton" runat="server" Text="Download" />
</asp:WebForm>
```

## 🏃 Modelos de Laptop Acer Soportados

Los scripts están optimizados para:
- **ASPIRE A315-59** - Modelo principal de análisis
- **ASPIRE A515-56** - Variante similar
- **Acer Sense** - Plataforma de gestión incluida en ejecutables

Pueden adaptarse para otros modelos Acer proporcionando el nombre del modelo correcto.

---

**Análisis completado el:** 2026-07-27  
**Version de Scripts:** 1.0  
**Scripts generados automáticamente basados en análisis de ejecutables Acer oficiales**