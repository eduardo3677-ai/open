# Acer Factory Image Download Analysis

## Executive Summary

This analysis examines downloaded Acer software packages to identify the infrastructure and logic used for software downloads, with particular focus on factory image downloads for the Acer Aspire A315-59 laptop.

## Download Infrastructure Discovered

### Primary Device Information API Endpoints

1. **Production server**: `https://device-info-prd-imub2p4wyq-uc.a.run.app`
   - Google Cloud Run infrastructure
   - Handles production device queries

2. **UAT server**: `https://device-info-uat-ycrmvsk7ia-uc.a.run.app`
   - User Acceptance Testing endpoint
   - Same infrastructure as production

### Download Client Components

The following HTTP client libraries and functions were identified:
- `httplib` - HTTP client implementation
- `WININET.dll` - Windows Internet API
- `WS2_32.dll` - Windows Socket API
- `HttpOpenRequestW`, `HttpEndRequestW`, `HttpSendRequestExW` - Core HTTP functions

### Key Executables for Download Logic

1. **AcerDIAgent.exe** - Device Information Agent
   - Primary agent for device information queries
   - Contains the device-info API connections
   - Entry point: 0x2F14C4, Image Base: 0x140000000

2. **AcerCCAgent.exe** - Care Center Agent
   - Handles software updates and downloads
   - Manages content download operations
   - Entry point: 0x280078

3. **AcerQAAgent.exe** - Quick Access Agent
   - Secondary download agent with similar capabilities
   - Contains `DownloadTask` class and `AsyncUpdater` functionality

## HTTP Headers and Content Types Detected

- `Content-Type: multipart/form-data`
- `Content-Type: application/x-www-form-urlencoded`
- Standard `Accept` headers
- `Cookie` handling capabilities
- Custom `User-Agent` strings

## Security Architecture

### Cryptographic Libraries
- `CRYPT32.dll` - Crypto API
- `bcrypt.dll` - Next Generation Crypto API
- OpenSSL components

### Certificate Authorities
- Sectigo (formerly Comodo)
- GlobalSign

### Security Features
- Code signing verification
- SSL/TLS encryption
- Certificate revocation checking (CRL/OCSP)

## Factory Image Download Workflow Hypothesis

Based on the analysis, the factory image download process likely follows this workflow:

1. **Device Identification**
   - Collect device information via device-info APIs
   - Submit device details (SNID, model, configuration)

2. **Image Availability Query**
   - Request factory image availability from Acer servers
   - Check compatibility based on device model

3. **Download Execution**
   - Download factory image from validated endpoint
   - Handle multi-part downloads with integrity checking

4. **Verification**
   - Verify digital signatures
   - Check file integrity using cryptographic checksums

## Configuration Files Identified

### Setup Configuration
- File: `Setup.exe.config`
- Contains package information and dependency requirements
- Version: 4.00.3060

### Service Configuration
- File: `AcerServiceWrapper.xml`
- Service ID: AcerService
- Log path: `C:\ProgramData\OEM\AcerService`

## Recommended Next Steps for Factory Image Download

### 1. Direct API Testing
Test the device-info endpoints with various request formats:
```bash
# Test UAT endpoint (safer for experimentation)
curl -X POST https://device-info-uat-ycrmvsk7ia-uc.a.run.app \
  -H "Content-Type: application/json" \
  -d '{"device_model":"ASPIRE A315-59"}'

# Test with common headers
curl -X POST https://device-info-uat-ycrmvsk7ia-uc.a.run.app \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "User-Agent: AcerDIAgent/1.0" \
  -d "model=ASPIRE+A315-59"
```

### 2. Deep Reverse Engineering
Perform more detailed analysis on `AcerDIAgent.exe`:
- Extract and analyze string resources
- Look for hardcoded API keys or authentication tokens
- Identify the exact request/response format

### 3. Network Traffic Analysis
Monitor actual network traffic during software updates:
- Use Wireshark or similar tools on a system with Acer software installed
- Capture and analyze HTTP requests/responses
- Identify index files or manifest files listing available downloads

### 4. Configuration File Search
Look for additional configuration files that may contain:
- API endpoints and authentication parameters
- Download server URLs
- Factory image repository information

### 5. Index File Investigation
Search for potential index or manifest files:
- Look for JSON/XML files listing available downloads
- Check for API endpoints that return downloadable content lists
- Investigate any "file index" or "download center" functionality

## Key Findings Summary

| Component | Purpose | Key Details |
|-----------|---------|-------------|
| device-info-prd | Production API | Google Cloud Run, handles real device queries |
| device-info-uat | Testing API | Safe endpoint for experimentation |
| AcerDIAgent.exe | Main download agent | Contains API connections and download logic |
| WININET.dll | HTTP client | Core networking functionality |
| CRYPT32.dll | Crypto ops | Signature verification |

## Conclusion

The analysis has identified the core infrastructure used by Acer for software downloads, including dedicated device information APIs hosted on Google Cloud. The `AcerDIAgent.exe` executable appears to be the key component containing the factory image download logic, with connections to both production and testing endpoints. Further investigation through API testing and network traffic analysis will likely reveal the complete workflow for obtaining factory images for the Acer Aspire A315-59.

## Analysis Methods Used

- Binary string extraction and pattern matching
- PE file structure analysis
- HTTP client library identification
- Configuration file examination
- Security component analysis

## Files Analyzed

- `AcerSense_Acer_5.0.1752_W11x64_A.zip` (301 MB)
- `Acer Care Center_Acer_4.00.3060_W11x64_A.zip` (76 MB)
- Multiple executables: `AcerDIAgent.exe`, `AcerCCAgent.exe`, `AcerQAAgent.exe`
- Configuration files: `Setup.exe.config`, `AcerServiceWrapper.xml`

---
*Analysis completed on 2026-07-27*