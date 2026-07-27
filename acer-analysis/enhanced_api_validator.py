#!/usr/bin/env python3
"""
Enhanced API Parameter Validation Script
Validates and tests Acer API parameter structure and logic
"""

import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class APIParameterValidator:
    def __init__(self):
        self.validation_rules = {}
        self.validated_params = []
        self.error_log = []
        
    def load_validation_rules(self):
        """Load validation rules from analysis data"""
        self.validation_rules = {
            "acerid": {
                "pattern": r'^[A-Za-z0-9\-_]{20,64}$',
                "required": True,
                "purpose": "Acer device identifier",
                "example": "A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6"
            },
            "SNID": {
                "pattern": r'^[A-Za-z0-9]{8,20}$',
                "required": True,
                "purpose": "Serial Number ID",
                "example": "LX123456789"
            },
            "Model": {
                "pattern": r'^[A-Za-z0-9\-\s]{5,50}$',
                "required": True,
                "purpose": "Device model identifier",
                "example": "ASPIRE A315-59"
            },
            "OS": {
                "pattern": r'^(Win10|Win11|Win8|Win7)$',
                "required": False,
                "purpose": "Operating system version",
                "example": "Win11"
            },
            "LC": {
                "pattern": r'^[A-Za-z]{2}$',
                "required": False,
                "purpose": "Language/Location Code",
                "example": "EN"
            },
            "BC": {
                "pattern": r'^[A-Za-z0-9_]{2,10}$',
                "required": False,
                "purpose": "Business Category",
                "example": "NB"
            },
            "SC": {
                "pattern": r'^[A-Za-z0-9_]{2,10}$',
                "required": False,
                "purpose": "Subcategory",
                "example": "G"
            },
            "Step1": {
                "pattern": r'^[A-Za-z0-9_\-\s]{1,100}$',
                "required": False,
                "purpose": "Workflow parameter step 1",
                "example": "Recovery"
            },
            "Step2": {
                "pattern": r'^[A-Za-z0-9_\-\s]{1,100}$',
                "required": False,
                "purpose": "Workflow parameter step 2",
                "example": "Download"
            },
            "Step3": {
                "pattern": r'^[A-Za-z0-9_\-\s]{1,100}$',
                "required": False,
                "purpose": "Workflow parameter step 3",
                "example": "Image"
            },
            "UUID": {
                "pattern": r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$',
                "required": False,
                "purpose": "System unique identifier",
                "example": "12345678-1234-1234-1234-1234567890AB"
            }
        }
        
    def validate_parameter(self, param_name: str, param_value: str) -> bool:
        """Validate a single parameter against its rule"""
        if param_name not in self.validation_rules:
            self.error_log.append(f"Unknown parameter: {param_name}")
            return False
            
        rule = self.validation_rules[param_name]
        pattern = rule['pattern']
        
        if not re.match(pattern, str(param_value)):
            error_msg = f"Invalid {param_name}: '{param_value}' does not match {pattern}"
            self.error_log.append(error_msg)
            return False
            
        self.validated_params.append({
            "name": param_name,
            "value": param_value,
            "status": "valid",
            "purpose": rule['purpose']
        })
        
        return True
    
    def validate_request_parameters(self, params: Dict[str, str]) -> bool:
        """Validate all parameters in a request"""
        all_valid = True
        
        # Check required parameters
        for param_name, rule in self.validation_rules.items():
            if rule['required'] and param_name not in params:
                self.error_log.append(f"Missing required parameter: {param_name}")
                all_valid = False
                
        # Validate provided parameters
        for param_name, param_value in params.items():
            if not self.validate_parameter(param_name, param_value):
                all_valid = False
                
        return all_valid
    
    def generate_parameter_template(self, required_only: bool = False) -> Dict[str, str]:
        """Generate parameter template for testing"""
        template = {}
        
        for param_name, rule in self.validation_rules.items():
            if not required_only or rule['required']:
                template[param_name] = rule['example']
                
        return template
    
    def create_request_url(self, base_url: str, params: Dict[str, str]) -> str:
        """Create complete request URL with parameters"""
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{query_string}"
    
    def analyze_request_patterns(self) -> List[Dict[str, str]]:
        """Analyze common request patterns"""
        patterns = []
        
        # Device information request pattern
        patterns.append({
            "pattern_name": "Device Info Request",
            "method": "POST",
            "url": "https://device-info-prd-imub2p4wyq-uc.a.run.app",
            "required_params": ["acerid", "SNID", "Model"],
            "optional_params": ["OS", "UUID"],
            "content_type": "application/x-www-form-urlencoded"
        })
        
        # Download request pattern
        patterns.append({
            "pattern_name": "Download Request",
            "method": "GET",
            "url": "https://global-download.acer.com/GDFiles/Recovery/",
            "required_params": ["acerid", "Model"],
            "optional_params": ["OS", "LC", "BC", "SC"],
            "content_type": "application/x-www-form-urlencoded"
        })
        
        # Version check pattern
        patterns.append({
            "pattern_name": "Version Check",
            "method": "POST",
            "url": "https://updates.acer.com/api/v1/version-check",
            "required_params": ["Model", "current_version"],
            "optional_params": ["acerid"],
            "content_type": "application/json"
        })
        
        return patterns
    
    def validate_endpoint_access(self, endpoint_url: str) -> bool:
        """Validate endpoint URL structure"""
        valid_domains = [
            'acer.com',
            '*.a.run.app',
            'global-download.acer.com'
        ]
        
        try:
            from urllib.parse import urlparse
            parsed = urlparse(endpoint_url)
            domain = parsed.netloc
            
            # Check against known valid domains
            for valid_domain in valid_domains:
                if valid_domain == domain or (valid_domain.startswith('*') and domain.endswith(valid_domain[1:])):
                    return True
                    
            self.error_log.append(f"Unrecognized endpoint domain: {domain}")
            return False
            
        except Exception as e:
            self.error_log.append(f"URL validation error: {str(e)}")
            return False
    
    def generate_validation_report(self) -> Dict:
        """Generate comprehensive validation report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "validation_summary": {
                "total_parameters": len(self.validation_rules),
                "required_parameters": sum(1 for r in self.validation_rules.values() if r['required']),
                "validated_parameters": len(self.validated_params)
            },
            "validation_errors": self.error_log,
            "validated_parameters": self.validated_params,
            "request_patterns": self.analyze_request_patterns(),
            "parameter_template": self.generate_parameter_template(required_only=True)
        }
        
        return report

def main():
    """Main execution function"""
    print("Enhanced API Parameter Validation Tool")
    print("=" * 50)
    
    validator = APIParameterValidator()
    validator.load_validation_rules()
    
    # Test parameter validation
    print("\nTesting parameter validation...")
    test_params = {
        "acerid": "A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6",
        "SNID": "LX123456789",
        "Model": "ASPIRE A315-59",
        "OS": "Win11",
        "LC": "EN"
    }
    
    is_valid = validator.validate_request_parameters(test_params)
    print(f"Parameter validation result: {'✓ Valid' if is_valid else '✗ Invalid'}")
    
    # Generate request URL
    print("\nGenerating sample download URL...")
    base_url = "https://global-download.acer.com/GDFiles/Recovery/"
    download_url = validator.create_request_url(base_url, test_params)
    print(f"Download URL: {download_url}")
    
    # Analyze request patterns
    print("\nAnalyzing request patterns...")
    patterns = validator.analyze_request_patterns()
    for pattern in patterns:
        print(f"\n  Pattern: {pattern['pattern_name']}")
        print(f"  Method: {pattern['method']}")
        print(f"  URL: {pattern['url']}")
        print(f"  Required Params: {', '.join(pattern['required_params'])}")
    
    # Generate validation report
    print("\nGenerating validation report...")
    report = validator.generate_validation_report()
    
    output_path = Path("api_parameter_validation_report.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"Validation report saved to: {output_path}")
    
    print("\nValidation Summary:")
    print(f"  Total Parameters: {report['validation_summary']['total_parameters']}")
    print(f"  Required Parameters: {report['validation_summary']['required_parameters']}")
    print(f"  Validated Parameters: {report['validation_summary']['validated_parameters']}")
    print(f"  Request Patterns: {len(report['request_patterns'])}")
    print(f"  Validation Errors: {len(report['validation_errors'])}")

if __name__ == "__main__":
    main()