# Acer Network Endpoints Documentation

## Overview
This document documents the network endpoints and protocols discovered during the analysis of Acer software packages.

## Discovered Server Endpoints

### Device Information Servers
```
https://device-info-uat-ycrmvsk7ia-uc.a.run.app
https://device-info-prd-imub2p4wyq-uc.a.run.app
```

**Purpose:** Acer device information collection servers  
**Protocol:** HTTPS  
**Hosting:** Google Cloud Run (*.a.run.app)  

### Known Acer Infrastructure
```
https://global-download.acer.com
```

**Purpose:** Main Acer download server  
**Known Paths:**  
- `/GDFiles/BIOS/` - BIOS downloads  
- `/GDFiles/Recovery/` - Recovery downloads  
- `/GDFiles/Factory/` - Factory images  

## Network Communication Protocols

### Transport Layer
- **Protocol:** HTTPS/TLS 1.2+
- **Libraries:** OpenSSL (libssl-3-x64.dll, libcrypto-3-x64.dll)
- **Certificate Validation:** Present and active

### Application Layer
- **HTTP Version:** HTTP/1.1
- **Request Methods:** POST, GET
- **Content-Type:** application/x-www-form-urlencoded

### Standard HTTP Headers Identified
- User-Agent
- Content-Type
- Cookie
- Authorization
- Content-Length

## Network Security Features

### Cryptographic Components
- SSL/TLS certificates embedded in executables
- Certificate validation mechanisms
- OpenSSL library usage

### Security Analysis
- ✅ Valid SSL certificates
- ✅ Signed executables by Acer
- ✅ Encrypted communications
- ⚠️ Hard-coded server endpoints

## Software Components with Network Capabilities

### AcerDIAgent.exe
- **Purpose:** Device Information Agent
- **Size:** ~5.6MB
- **Capabilities:** Hardware inventory, network communication

### AcerCCAgent.exe  
- **Purpose:** Cloud Control Agent
- **Size:** ~5.6MB
- **Capabilities:** Cloud management, remote configuration

### AcerQAAgent.exe
- **Purpose:** Quick Access Agent
- **Size:** ~10MB
- **Capabilities:** User interface, hardware control, system monitoring

## Network Libraries Found

### Core Libraries
- **OpenSSL:** libssl-3-x64.dll, libcrypto-3-x64.dll
- **cURL:** cares.dll (HTTP operations)
- **Compression:** brotlicommon.dll, brotlidec.dll, brotlienc.dll

### Windows Networking
- WinINet/WinHTTP APIs
- Windows Sockets API

## API Parameter Conventions

### Identified URL Parameters
Based on analysis of Acer download URLs:
- `acerid` - Acer identifier
- `Step1` - Parameter step 1
- `Step2` - Parameter step 2  
- `Step3` - Parameter step 3
- `OS` - Operating system version
- `LC` - Location code
- `BC` - Product category
- `SC` - Product subcategory

## Traffic Patterns

### Update Mechanisms
- Version checking protocols
- NewVersionInstalled events
- SameVersionExisted handling
- OlderVersionExisted fallbacks

### Registry Integration
- UnInstallKeyURLUpdateInfo registry key
- ACCVersionUpdate functions
- RegUpdate functions

## Device Identification

### Hardware Information Gathering
- AcerSMBIOS components
- AcerWMI components
- Model identification capabilities
- SNID/UUID collection

## Testing Notes

### Endpoint Availability
- HTTPS connectivity required
- Certificate chain validation
- Proper User-Agent headers needed
- Device identification parameters required

### Network Requirements
- Internet connectivity
- DNS resolution to acer.com and *.a.run.app
- SSL/TLS handshake capability
- Firewall rules allowing outbound HTTPS

## Security Considerations

### Best Practices
- Always verify SSL certificates
- Use proper authentication when required
- Monitor for unauthorized access attempts
- Keep software updated with official patches

### Limitations
- Some endpoints may require device-specific authentication
- Factory images may have additional access controls
- Rate limiting may apply to public endpoints

## Reference Information

### Analysis Date
- Analysis performed: 2026-07-27
- Software versions analyzed: AcerSense 5.0.1752, Acer Care Center 4.00.3060

### Analysis Tools
- Python pefile library
- Capstone disassembly framework
- String extraction utilities
- Binary pattern matching

---

## Appendix: Known Dependencies

### Required Libraries for Network Operations
- OpenSSL 3.x
- Windows networking libraries
- cURL with SSL support
- Brotli compression library

### Supported File Types
- .exe (Windows executables)
- .zip (compressed archives)
- .rar (compressed archives)
- .7z (compressed archives)
- .msi (Windows installer packages)
- .bin (binary files)

---

*This documentation is based on static analysis of Acer software packages and public information.*