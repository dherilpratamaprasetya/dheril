#!/usr/bin/env python3
"""
IoT Dashboard API Test Script
Test all API endpoints with sample data
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api"

def test_api():
    print("🧪 Testing IoT Dashboard API...")
    
    # Test 1: Add sensor data
    print("\n1. Adding sample sensor data...")
    
    # Add gas data
    gas_data = {
        "sensor_type": "gas",
        "value": 250.5,
        "status": "warning"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/sensors/", json=gas_data)
        print(f"   Gas data: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"   Error adding gas data: {e}")
    
    # Add temperature data
    temp_data = {
        "sensor_type": "temperature",
        "value": 28.5,
        "status": "normal"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/sensors/", json=temp_data)
        print(f"   Temp data: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"   Error adding temp data: {e}")
    
    # Test 2: Get all sensors
    print("\n2. Getting all sensor data...")
    try:
        response = requests.get(f"{BASE_URL}/sensors/")
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Count: {len(data.get('results', []))}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Get latest data
    print("\n3. Getting latest sensor data...")
    try:
        response = requests.get(f"{BASE_URL}/sensors/latest/")
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Latest data: {json.dumps(data, indent=2)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Get statistics
    print("\n4. Getting sensor statistics...")
    try:
        response = requests.get(f"{BASE_URL}/sensors/stats/")
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Stats: {json.dumps(data, indent=2)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 5: Update threshold
    print("\n5. Updating thresholds...")
    threshold_data = {
        "sensor_type": "gas",
        "warning_min": 0,
        "warning_max": 300,
        "danger_min": 300,
        "danger_max": 1000
    }
    
    try:
        response = requests.post(f"{BASE_URL}/settings/threshold/", json=threshold_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 6: Get alerts
    print("\n6. Getting alerts...")
    try:
        response = requests.get(f"{BASE_URL}/alerts/")
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Alerts count: {len(data)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n✅ API testing completed!")

if __name__ == "__main__":
    print("Make sure Django server is running: python manage.py runserver")
    print("Press Enter to start testing...")
    input()
    test_api()