#!/usr/bin/env python3
"""
Test script for the Beehiiv Integration API
Run this script to test the API endpoints locally
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = "http://localhost:8000"  # Change this to your deployed URL
TEST_EMAIL = "test@example.com"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_subscribe_endpoint():
    """Test the subscribe endpoint"""
    print("\nTesting subscribe endpoint...")
    try:
        payload = {
            "email": TEST_EMAIL,
            "first_name": "Test",
            "last_name": "User",
            "source": "test"
        }
        
        response = requests.post(
            f"{BASE_URL}/subscribe",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_publication_info():
    """Test the publication info endpoint"""
    print("\nTesting publication info endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/publication-info")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print("Beehiiv Integration API Test Suite")
    print("=" * 40)
    
    # Check if environment variables are set
    if not os.getenv("BEEHIIV_API_KEY"):
        print("Warning: BEEHIIV_API_KEY not set in environment")
    if not os.getenv("BEEHIIV_PUBLICATION_ID"):
        print("Warning: BEEHIIV_PUBLICATION_ID not set in environment")
    
    # Run tests
    tests = [
        ("Health Check", test_health_endpoint),
        ("Subscribe Endpoint", test_subscribe_endpoint),
        ("Publication Info", test_publication_info)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 20)
        success = test_func()
        results.append((test_name, success))
    
    # Summary
    print("\n" + "=" * 40)
    print("Test Results Summary:")
    print("=" * 40)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    total_passed = sum(1 for _, success in results if success)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")

if __name__ == "__main__":
    main()
