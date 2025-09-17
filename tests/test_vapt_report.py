"""
Test VAPT Report Generation
===========================

Simple test script to generate a sample VAPT report without requiring 
OpenSearch or CrewAI dependencies.
"""

import sys
import os
from datetime import datetime, timezone
import json

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from pentest_app.reports.vapt_final import VAPTFinalReport

def create_sample_findings():
    """Create sample findings for testing the report generation."""
    sample_findings = [
        {
            'severity': 'critical',
            'title': 'SQL Injection Vulnerability',
            'description': 'The application is vulnerable to SQL injection attacks through the user login form. Malicious SQL code can be injected through the username parameter, potentially allowing unauthorized access to the database.',
            'recommendation': 'Implement parameterized queries and input validation. Use prepared statements and escape user input properly.',
            'tool': 'SQLMap',
            'timestamp': datetime.now(timezone.utc),
            'cvss': '9.8',
            'affected_system': 'https://juice-shop.herokuapp.com',
            'impact': 'Critical: This vulnerability could allow complete database compromise, data theft, and unauthorized administrative access.'
        },
        {
            'severity': 'high',
            'title': 'Cross-Site Scripting (XSS)',
            'description': 'Stored XSS vulnerability found in the product review section. User input is not properly sanitized before being stored and displayed to other users.',
            'recommendation': 'Implement output encoding and content security policy. Validate and sanitize all user inputs.',
            'tool': 'OWASP ZAP',
            'timestamp': datetime.now(timezone.utc),
            'cvss': '8.1',
            'affected_system': 'https://juice-shop.herokuapp.com',
            'impact': 'High: This vulnerability could allow session hijacking, credential theft, and malicious content injection.'
        },
        {
            'severity': 'medium',
            'title': 'Weak Password Policy',
            'description': 'The application allows users to set weak passwords without enforcing complexity requirements.',
            'recommendation': 'Implement strong password policy requiring minimum length, complexity, and regular rotation.',
            'tool': 'Manual Review',
            'timestamp': datetime.now(timezone.utc),
            'cvss': '5.3',
            'affected_system': 'https://juice-shop.herokuapp.com',
            'impact': 'Medium: Weak passwords increase the risk of brute force attacks and account compromise.'
        },
        {
            'severity': 'low',
            'title': 'Information Disclosure',
            'description': 'Server response headers reveal information about the technology stack and server version.',
            'recommendation': 'Configure the web server to hide version information and remove unnecessary response headers.',
            'tool': 'Nmap',
            'timestamp': datetime.now(timezone.utc),
            'cvss': '3.1',
            'affected_system': 'https://juice-shop.herokuapp.com',
            'impact': 'Low: Information disclosure may assist attackers in reconnaissance activities.'
        },
        {
            'severity': 'info',
            'title': 'HTTP Security Headers Missing',
            'description': 'Some recommended HTTP security headers are missing, including Content-Security-Policy and X-Frame-Options.',
            'recommendation': 'Implement comprehensive HTTP security headers to enhance browser-side security.',
            'tool': 'Nikto',
            'timestamp': datetime.now(timezone.utc),
            'cvss': 'N/A',
            'affected_system': 'https://juice-shop.herokuapp.com',
            'impact': 'Informational: Missing security headers may leave the application vulnerable to certain client-side attacks.'
        }
    ]
    
    return sample_findings

def test_vapt_report_generation():
    """Test the VAPT report generation functionality."""
    try:
        print("[START] Starting VAPT Report Generation Test...")
        
        # Generate a test run ID
        run_id = "test-run-12345"
        target = "https://juice-shop.herokuapp.com"
        
        print(f"[INFO] Test Parameters:")
        print(f"   Run ID: {run_id}")
        print(f"   Target: {target}")
        
        # Create VAPT report generator
        print("\n[BUILD]  Initializing VAPT Report Generator...")
        vapt_generator = VAPTFinalReport(
            run_id=run_id,
            target=target,
            output_dir="reports"
        )
        
        # Add sample findings
        print("[ADD] Adding sample security findings...")
        sample_findings = create_sample_findings()
        
        for finding in sample_findings:
            vapt_generator.add_finding(finding)
        
        print(f"   Added {len(sample_findings)} findings:")
        for severity, count in vapt_generator.summary_stats.items():
            if count > 0:
                print(f"   - {severity.title()}: {count}")
        
        # Calculate risk assessment
        print("\n[CALC] Calculating risk assessment...")
        risk_score = vapt_generator.calculate_overall_risk()
        print(f"   Overall Risk Score: {risk_score:.2f}/10.0")
        print(f"   Risk Rating: {vapt_generator.risk_rating}")
        
        # Generate AI insights
        print("\n[AI] Generating AI insights...")
        vapt_generator.add_ai_insights()
        
        # Generate the report
        print("\n[GEN] Generating PDF report...")
        report_path = vapt_generator.generate_report()
        
        # Verify the report was created
        if os.path.exists(report_path):
            file_size = os.path.getsize(report_path) / 1024  # Size in KB
            print(f"[SUCCESS] Report generated successfully!")
            print(f"   File: {report_path}")
            print(f"   Size: {file_size:.1f} KB")
            
            # Get report metadata
            metadata = vapt_generator.get_report_metadata()
            print(f"\n[META] Report Metadata:")
            print(f"   Total Findings: {metadata['total_findings']}")
            print(f"   Risk Score: {metadata['overall_risk_score']:.2f}")
            print(f"   Risk Rating: {metadata['risk_rating']}")
            print(f"   Filename: {metadata['filename']}")
            
            return True
        else:
            print("[ERROR] Report generation failed - file not created")
            return False
            
    except Exception as e:
        print(f"[ERROR] Test failed with error: {str(e)}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")
        return False

def main():
    """Main test function."""
    print("=" * 60)
    print("VAPT Report Generation Test")
    print("=" * 60)
    
    success = test_vapt_report_generation()
    
    print("\n" + "=" * 60)
    if success:
        print("[COMPLETE] Test completed successfully!")
        print("[SUCCESS] VAPT report generation system is working correctly.")
    else:
        print("[ERROR] Test failed!")
        print("🔧 Check the error messages above for troubleshooting.")
    print("=" * 60)
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())