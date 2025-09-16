#!/usr/bin/env python3
"""
Simple API Test Script for Penetration Testing Framework
========================================================

This script tests the API endpoints without requiring all dependencies.
"""

import json
import urllib.request
import urllib.parse
import time

API_BASE = "http://localhost:8000"

def make_request(url, method="GET", data=None):
    """Make HTTP request and return response."""
    try:
        if data:
            data = json.dumps(data).encode('utf-8')
        
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

def test_api():
    """Test the penetration testing API."""
    print("🔐 Testing Penetration Testing Framework API")
    print("=============================================")
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    health = make_request(f"{API_BASE}/health")
    if health:
        print("✅ Health Check Response:")
        print(json.dumps(health, indent=2))
    else:
        print("❌ Health check failed. Make sure API is running:")
        print("   uvicorn main:app --reload")
        return
    
    # Test 2: Authorized Targets
    print("\n2. Getting Authorized Targets...")
    targets = make_request(f"{API_BASE}/authorized_targets")
    if targets:
        print("✅ Authorized Targets:")
        print(json.dumps(targets, indent=2))
    
    # Test 3: Start Penetration Test
    print("\n3. Starting Penetration Test...")
    payload = {
        "target": "https://juice-shop.herokuapp.com",
        "consent_acknowledged": True
    }
    
    print("📤 Sending request:")
    print(json.dumps(payload, indent=2))
    
    response = make_request(f"{API_BASE}/invoke_pentest", "POST", payload)
    if response:
        print("✅ Penetration Test Started!")
        print(json.dumps(response, indent=2))
        
        run_id = response.get('run_id')
        if run_id:
            print(f"\n📋 Run ID: {run_id}")
            
            # Test 4: Check Status
            print("\n4. Checking Test Status...")
            time.sleep(2)
            
            status = make_request(f"{API_BASE}/pentest_status/{run_id}")
            if status:
                print("✅ Status Response:")
                print(json.dumps(status, indent=2))
    
    print("\n🔗 Useful Commands:")
    print("  - Start API: uvicorn main:app --reload")
    print("  - View Docs: http://localhost:8000/docs")
    print("  - OpenSearch: https://cybrty-dev-ca.wonderfuldune-e921120d.eastus.azurecontainerapps.io")

if __name__ == "__main__":
    test_api()