import os
import json
import subprocess
import tempfile
import time
from urllib.parse import urlparse
import logging

class WASScanner:
    """Web Application Security Scanner (Mock Only)"""
    def __init__(self):
        pass

    def scan_url(self, target_url):
        """Always use mock scan for vulnerabilities (no subprocess, no ZAP check)"""
        return self._mock_was_scan(target_url)
    
    def _mock_was_scan(self, target_url):
        """Mock WAS scan results for demonstration"""
        import random
        
        vulnerabilities = [
            {
                'name': 'Cross-Site Scripting (XSS)',
                'severity': 'High',
                'description': 'Potential XSS vulnerability detected in input fields',
                'location': f'{target_url}/search',
                'confidence': 'Medium',
                'risk': 'High',
                'cwe': 'CWE-79',
                'solution': 'Implement proper input validation and output encoding'
            },
            {
                'name': 'SQL Injection',
                'severity': 'Critical',
                'description': 'Possible SQL injection vulnerability in login form',
                'location': f'{target_url}/login',
                'confidence': 'High',
                'risk': 'Critical',
                'cwe': 'CWE-89',
                'solution': 'Use parameterized queries and input validation'
            },
            {
                'name': 'Missing Security Headers',
                'severity': 'Medium',
                'description': 'Security headers are missing or misconfigured',
                'location': target_url,
                'confidence': 'High',
                'risk': 'Medium',
                'cwe': 'CWE-16',
                'solution': 'Implement security headers like CSP, HSTS, X-Frame-Options'
            },
            {
                'name': 'Insecure Direct Object Reference',
                'severity': 'High',
                'description': 'Direct object references without proper authorization',
                'location': f'{target_url}/user/profile',
                'confidence': 'Medium',
                'risk': 'High',
                'cwe': 'CWE-639',
                'solution': 'Implement proper access controls and authorization checks'
            }
        ]
        
        # Randomly select some vulnerabilities
        selected_vulns = random.sample(vulnerabilities, k=random.randint(1, len(vulnerabilities)))
        
        return {
            'target': target_url,
            'scan_type': 'web_application_security',
            'timestamp': time.time(),
            'summary': {
                'total_vulnerabilities': len(selected_vulns),
                'critical': len([v for v in selected_vulns if v['severity'] == 'Critical']),
                'high': len([v for v in selected_vulns if v['severity'] == 'High']),
                'medium': len([v for v in selected_vulns if v['severity'] == 'Medium']),
                'low': len([v for v in selected_vulns if v['severity'] == 'Low'])
            },
            'vulnerabilities': selected_vulns
        }
    
    def _process_zap_results(self, zap_alerts, target_url):
        """Process ZAP scan results into standardized format"""
        vulnerabilities = []
        
        for alert in zap_alerts.get('alerts', []):
            vuln = {
                'name': alert.get('alert', 'Unknown'),
                'severity': alert.get('risk', 'Unknown'),
                'description': alert.get('description', ''),
                'location': alert.get('url', target_url),
                'confidence': alert.get('confidence', 'Unknown'),
                'risk': alert.get('risk', 'Unknown'),
                'cwe': alert.get('cweid', ''),
                'solution': alert.get('solution', '')
            }
            vulnerabilities.append(vuln)
        
        return {
            'target': target_url,
            'scan_type': 'web_application_security',
            'timestamp': time.time(),
            'summary': {
                'total_vulnerabilities': len(vulnerabilities),
                'critical': len([v for v in vulnerabilities if v['severity'] == 'High']),
                'high': len([v for v in vulnerabilities if v['severity'] == 'Medium']),
                'medium': len([v for v in vulnerabilities if v['severity'] == 'Low']),
                'low': len([v for v in vulnerabilities if v['severity'] == 'Informational'])
            },
            'vulnerabilities': vulnerabilities
        }

class IaCScanner:
    """Infrastructure as Code Scanner using Checkov"""
    
    def __init__(self):
        self.checkov_available = self._check_checkov()
    
    def _check_checkov(self):
        """Check if Checkov is available"""
        try:
            result = subprocess.run(['checkov', '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            logging.warning("Checkov not found, using mock implementation")
            return False
    
    def scan_file(self, file_path):
        """Scan an IaC file for misconfigurations"""
        if not self.checkov_available:
            return self._mock_iac_scan(file_path)
        
        try:
            # Run Checkov scan
            result = subprocess.run([
                'checkov',
                '--file', file_path,
                '--output', 'json',
                '--quiet'
            ], capture_output=True, text=True)
            
            if result.returncode != 0 and result.stdout:
                # Parse Checkov results
                checkov_results = json.loads(result.stdout)
                return self._process_checkov_results(checkov_results, file_path)
            else:
                return self._mock_iac_scan(file_path)
                
        except Exception as e:
            logging.error(f"IaC scan failed: {str(e)}")
            return self._mock_iac_scan(file_path)
    
    def _mock_iac_scan(self, file_path):
        """Mock IaC scan results for demonstration"""
        import random
        
        misconfigurations = [
            {
                'check_id': 'CKV_AWS_20',
                'check_name': 'S3 Bucket public read acl',
                'severity': 'High',
                'description': 'S3 bucket should not have public read access',
                'file_path': file_path,
                'line_range': [15, 25],
                'resource': 'aws_s3_bucket.example',
                'guideline': 'Remove public read access from S3 bucket ACL',
                'remediation': 'Set bucket ACL to private and use bucket policies for controlled access'
            },
            {
                'check_id': 'CKV_AWS_21',
                'check_name': 'S3 Bucket versioning',
                'severity': 'Medium',
                'description': 'S3 bucket should have versioning enabled',
                'file_path': file_path,
                'line_range': [30, 35],
                'resource': 'aws_s3_bucket.example',
                'guideline': 'Enable versioning on S3 bucket',
                'remediation': 'Add versioning configuration to S3 bucket resource'
            },
            {
                'check_id': 'CKV_AWS_8',
                'check_name': 'Launch configuration security group',
                'severity': 'Critical',
                'description': 'Launch configuration should not have security group with 0.0.0.0/0',
                'file_path': file_path,
                'line_range': [45, 55],
                'resource': 'aws_launch_configuration.example',
                'guideline': 'Restrict security group access',
                'remediation': 'Replace 0.0.0.0/0 with specific IP ranges or security groups'
            },
            {
                'check_id': 'CKV_AWS_2',
                'check_name': 'ALB listener HTTPS',
                'severity': 'High',
                'description': 'ALB listener should use HTTPS',
                'file_path': file_path,
                'line_range': [60, 70],
                'resource': 'aws_lb_listener.example',
                'guideline': 'Use HTTPS protocol for ALB listener',
                'remediation': 'Change protocol from HTTP to HTTPS and add SSL certificate'
            },
            {
                'check_id': 'CKV_AWS_23',
                'check_name': 'Security group SSH access',
                'severity': 'High',
                'description': 'Security group should not allow SSH access from 0.0.0.0/0',
                'file_path': file_path,
                'line_range': [75, 85],
                'resource': 'aws_security_group.example',
                'guideline': 'Restrict SSH access to specific IP ranges',
                'remediation': 'Replace 0.0.0.0/0 with specific IP addresses or ranges for SSH access'
            }
        ]
        
        # Randomly select some misconfigurations
        selected_issues = random.sample(misconfigurations, k=random.randint(2, len(misconfigurations)))
        
        return {
            'target': file_path,
            'scan_type': 'infrastructure_as_code',
            'timestamp': time.time(),
            'summary': {
                'total_issues': len(selected_issues),
                'critical': len([i for i in selected_issues if i['severity'] == 'Critical']),
                'high': len([i for i in selected_issues if i['severity'] == 'High']),
                'medium': len([i for i in selected_issues if i['severity'] == 'Medium']),
                'low': len([i for i in selected_issues if i['severity'] == 'Low'])
            },
            'issues': selected_issues
        }
    
    def _process_checkov_results(self, checkov_results, file_path):
        """Process Checkov results into standardized format"""
        issues = []
        
        for result in checkov_results.get('results', {}).get('failed_checks', []):
            issue = {
                'check_id': result.get('check_id', ''),
                'check_name': result.get('check_name', ''),
                'severity': self._map_severity(result.get('severity', 'MEDIUM')),
                'description': result.get('description', ''),
                'file_path': result.get('file_path', file_path),
                'line_range': result.get('file_line_range', []),
                'resource': result.get('resource', ''),
                'guideline': result.get('guideline', ''),
                'remediation': result.get('description', '')
            }
            issues.append(issue)
        
        return {
            'target': file_path,
            'scan_type': 'infrastructure_as_code',
            'timestamp': time.time(),
            'summary': {
                'total_issues': len(issues),
                'critical': len([i for i in issues if i['severity'] == 'Critical']),
                'high': len([i for i in issues if i['severity'] == 'High']),
                'medium': len([i for i in issues if i['severity'] == 'Medium']),
                'low': len([i for i in issues if i['severity'] == 'Low'])
            },
            'issues': issues
        }
    
    def _map_severity(self, checkov_severity):
        """Map Checkov severity to standardized severity levels"""
        mapping = {
            'CRITICAL': 'Critical',
            'HIGH': 'High',
            'MEDIUM': 'Medium',
            'LOW': 'Low',
            'INFO': 'Low'
        }
        return mapping.get(checkov_severity.upper(), 'Medium')
