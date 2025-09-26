#!/usr/bin/env python3
"""
TradingHub Backend API Test Suite
Comprehensive testing of all backend endpoints
"""

import asyncio
import httpx
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

# Get backend URL from environment
BACKEND_URL = "https://signalpro-1.preview.emergentagent.com/api"

class TradingHubAPITester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.client = None
        self.test_results = []
        
    async def __aenter__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
    
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    Details: {details}")
        if not success and response_data:
            print(f"    Response: {response_data}")
        print()
    
    async def test_health_endpoints(self):
        """Test basic health check endpoints"""
        print("=== TESTING HEALTH ENDPOINTS ===")
        
        # Test root endpoint
        try:
            response = await self.client.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "version" in data:
                    self.log_test("Root endpoint (/api/)", True, f"Status: {response.status_code}, Message: {data.get('message')}")
                else:
                    self.log_test("Root endpoint (/api/)", False, f"Missing required fields in response", data)
            else:
                self.log_test("Root endpoint (/api/)", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Root endpoint (/api/)", False, f"Exception: {str(e)}")
        
        # Test health endpoint
        try:
            response = await self.client.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                if "status" in data and data["status"] == "healthy":
                    self.log_test("Health endpoint (/api/health)", True, f"Status: {data.get('status')}")
                else:
                    self.log_test("Health endpoint (/api/health)", False, f"Unhealthy status", data)
            else:
                self.log_test("Health endpoint (/api/health)", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Health endpoint (/api/health)", False, f"Exception: {str(e)}")
    
    async def test_providers_api(self):
        """Test providers API endpoints"""
        print("=== TESTING PROVIDERS API ===")
        
        # Test GET /api/providers
        try:
            response = await self.client.get(f"{self.base_url}/providers/")
            if response.status_code == 200:
                data = response.json()
                if "success" in data and data["success"] and "data" in data:
                    providers = data["data"]
                    total = data.get("total", 0)
                    self.log_test("GET /api/providers", True, f"Retrieved {len(providers)} providers, Total: {total}")
                    
                    # Validate provider structure
                    if providers:
                        provider = providers[0]
                        required_fields = ["id", "name", "winRate", "signalTypes", "subscriptionPrice", "rating"]
                        missing_fields = [field for field in required_fields if field not in provider]
                        if not missing_fields:
                            self.log_test("Provider data structure", True, "All required fields present")
                        else:
                            self.log_test("Provider data structure", False, f"Missing fields: {missing_fields}")
                else:
                    self.log_test("GET /api/providers", False, "Invalid response structure", data)
            else:
                self.log_test("GET /api/providers", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("GET /api/providers", False, f"Exception: {str(e)}")
        
        # Test providers with filters
        filters = [
            ("signalType", "Forex"),
            ("riskLevel", "Baixo"),
            ("priceRange", "50-100"),
            ("search", "Alpha")
        ]
        
        for filter_name, filter_value in filters:
            try:
                params = {filter_name: filter_value}
                response = await self.client.get(f"{self.base_url}/providers", params=params)
                if response.status_code == 200:
                    data = response.json()
                    if "success" in data and data["success"]:
                        count = len(data.get("data", []))
                        self.log_test(f"Providers filter: {filter_name}={filter_value}", True, f"Retrieved {count} filtered providers")
                    else:
                        self.log_test(f"Providers filter: {filter_name}={filter_value}", False, "Invalid response", data)
                else:
                    self.log_test(f"Providers filter: {filter_name}={filter_value}", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"Providers filter: {filter_name}={filter_value}", False, f"Exception: {str(e)}")
        
        # Test pagination
        try:
            params = {"limit": 2, "skip": 0}
            response = await self.client.get(f"{self.base_url}/providers", params=params)
            if response.status_code == 200:
                data = response.json()
                if "success" in data and len(data.get("data", [])) <= 2:
                    self.log_test("Providers pagination", True, f"Limit respected: {len(data['data'])} items")
                else:
                    self.log_test("Providers pagination", False, "Pagination not working correctly")
            else:
                self.log_test("Providers pagination", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Providers pagination", False, f"Exception: {str(e)}")
        
        # Test search endpoint
        try:
            params = {"q": "Alpha", "limit": 10}
            response = await self.client.get(f"{self.base_url}/providers/search", params=params)
            if response.status_code == 200:
                data = response.json()
                if "success" in data and data["success"]:
                    count = len(data.get("data", []))
                    self.log_test("Providers search", True, f"Search returned {count} results")
                else:
                    self.log_test("Providers search", False, "Invalid search response", data)
            else:
                self.log_test("Providers search", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Providers search", False, f"Exception: {str(e)}")
        
        # Test individual provider by ID
        try:
            response = await self.client.get(f"{self.base_url}/providers/1")
            if response.status_code == 200:
                data = response.json()
                if "success" in data and data["success"] and "data" in data:
                    provider = data["data"]
                    self.log_test("GET provider by ID", True, f"Retrieved provider: {provider.get('name', 'Unknown')}")
                else:
                    self.log_test("GET provider by ID", False, "Invalid response structure", data)
            else:
                self.log_test("GET provider by ID", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("GET provider by ID", False, f"Exception: {str(e)}")
        
        # Test non-existent provider
        try:
            response = await self.client.get(f"{self.base_url}/providers/nonexistent")
            if response.status_code == 404:
                self.log_test("GET non-existent provider", True, "Correctly returned 404")
            else:
                self.log_test("GET non-existent provider", False, f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.log_test("GET non-existent provider", False, f"Exception: {str(e)}")
    
    async def test_brokers_api(self):
        """Test brokers API endpoints"""
        print("=== TESTING BROKERS API ===")
        
        # Test GET /api/brokers
        try:
            response = await self.client.get(f"{self.base_url}/brokers")
            if response.status_code == 200:
                data = response.json()
                if "success" in data and data["success"] and "data" in data:
                    brokers = data["data"]
                    total = data.get("total", 0)
                    self.log_test("GET /api/brokers", True, f"Retrieved {len(brokers)} brokers, Total: {total}")
                    
                    # Validate broker structure
                    if brokers:
                        broker = brokers[0]
                        required_fields = ["id", "name", "minDeposit", "maxLeverage", "rating", "regulation"]
                        missing_fields = [field for field in required_fields if field not in broker]
                        if not missing_fields:
                            self.log_test("Broker data structure", True, "All required fields present")
                        else:
                            self.log_test("Broker data structure", False, f"Missing fields: {missing_fields}")
                else:
                    self.log_test("GET /api/brokers", False, "Invalid response structure", data)
            else:
                self.log_test("GET /api/brokers", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("GET /api/brokers", False, f"Exception: {str(e)}")
        
        # Test brokers with filters
        filters = [
            ("instrumentType", "Forex"),
            ("minDeposit", "500"),
            ("regulation", "FCA"),
            ("search", "Trade")
        ]
        
        for filter_name, filter_value in filters:
            try:
                params = {filter_name: filter_value}
                response = await self.client.get(f"{self.base_url}/brokers", params=params)
                if response.status_code == 200:
                    data = response.json()
                    if "success" in data and data["success"]:
                        count = len(data.get("data", []))
                        self.log_test(f"Brokers filter: {filter_name}={filter_value}", True, f"Retrieved {count} filtered brokers")
                    else:
                        self.log_test(f"Brokers filter: {filter_name}={filter_value}", False, "Invalid response", data)
                else:
                    self.log_test(f"Brokers filter: {filter_name}={filter_value}", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"Brokers filter: {filter_name}={filter_value}", False, f"Exception: {str(e)}")
        
        # Test broker search
        try:
            params = {"q": "Trade", "limit": 10}
            response = await self.client.get(f"{self.base_url}/brokers/search", params=params)
            if response.status_code == 200:
                data = response.json()
                if "success" in data and data["success"]:
                    count = len(data.get("data", []))
                    self.log_test("Brokers search", True, f"Search returned {count} results")
                else:
                    self.log_test("Brokers search", False, "Invalid search response", data)
            else:
                self.log_test("Brokers search", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Brokers search", False, f"Exception: {str(e)}")
        
        # Test individual broker by ID
        try:
            response = await self.client.get(f"{self.base_url}/brokers/1")
            if response.status_code == 200:
                data = response.json()
                if "success" in data and data["success"] and "data" in data:
                    broker = data["data"]
                    self.log_test("GET broker by ID", True, f"Retrieved broker: {broker.get('name', 'Unknown')}")
                else:
                    self.log_test("GET broker by ID", False, "Invalid response structure", data)
            else:
                self.log_test("GET broker by ID", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("GET broker by ID", False, f"Exception: {str(e)}")
    
    async def test_testimonials_api(self):
        """Test testimonials API endpoints"""
        print("=== TESTING TESTIMONIALS API ===")
        
        # Test GET /api/testimonials
        try:
            response = await self.client.get(f"{self.base_url}/testimonials")
            if response.status_code == 200:
                data = response.json()
                if "success" in data and data["success"] and "data" in data:
                    testimonials = data["data"]
                    total = data.get("total", 0)
                    self.log_test("GET /api/testimonials", True, f"Retrieved {len(testimonials)} testimonials, Total: {total}")
                    
                    # Validate testimonial structure
                    if testimonials:
                        testimonial = testimonials[0]
                        required_fields = ["id", "name", "role", "rating", "text", "approved"]
                        missing_fields = [field for field in required_fields if field not in testimonial]
                        if not missing_fields:
                            self.log_test("Testimonial data structure", True, "All required fields present")
                        else:
                            self.log_test("Testimonial data structure", False, f"Missing fields: {missing_fields}")
                else:
                    self.log_test("GET /api/testimonials", False, "Invalid response structure", data)
            else:
                self.log_test("GET /api/testimonials", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("GET /api/testimonials", False, f"Exception: {str(e)}")
        
        # Test testimonials with approval filter
        try:
            params = {"approved": True}
            response = await self.client.get(f"{self.base_url}/testimonials", params=params)
            if response.status_code == 200:
                data = response.json()
                if "success" in data and data["success"]:
                    count = len(data.get("data", []))
                    self.log_test("Testimonials approved filter", True, f"Retrieved {count} approved testimonials")
                else:
                    self.log_test("Testimonials approved filter", False, "Invalid response", data)
            else:
                self.log_test("Testimonials approved filter", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Testimonials approved filter", False, f"Exception: {str(e)}")
        
        # Test individual testimonial by ID
        try:
            response = await self.client.get(f"{self.base_url}/testimonials/1")
            if response.status_code == 200:
                data = response.json()
                if "success" in data and data["success"] and "data" in data:
                    testimonial = data["data"]
                    self.log_test("GET testimonial by ID", True, f"Retrieved testimonial: {testimonial.get('name', 'Unknown')}")
                else:
                    self.log_test("GET testimonial by ID", False, "Invalid response structure", data)
            else:
                self.log_test("GET testimonial by ID", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("GET testimonial by ID", False, f"Exception: {str(e)}")
    
    async def test_auth_endpoints(self):
        """Test authentication endpoints"""
        print("=== TESTING AUTH ENDPOINTS ===")
        
        # Test auth check endpoint (should work without authentication)
        try:
            response = await self.client.get(f"{self.base_url}/auth/check")
            if response.status_code == 200:
                data = response.json()
                if "authenticated" in data:
                    auth_status = data["authenticated"]
                    self.log_test("GET /api/auth/check", True, f"Auth check successful, authenticated: {auth_status}")
                else:
                    self.log_test("GET /api/auth/check", False, "Missing authenticated field", data)
            else:
                self.log_test("GET /api/auth/check", False, f"Status: {response.status_code}", response.text)
        except Exception as e:
            self.log_test("GET /api/auth/check", False, f"Exception: {str(e)}")
        
        # Test /me endpoint without authentication (should return 401)
        try:
            response = await self.client.get(f"{self.base_url}/auth/me")
            if response.status_code == 401:
                self.log_test("GET /api/auth/me (no auth)", True, "Correctly returned 401 for unauthenticated request")
            else:
                self.log_test("GET /api/auth/me (no auth)", False, f"Expected 401, got {response.status_code}")
        except Exception as e:
            self.log_test("GET /api/auth/me (no auth)", False, f"Exception: {str(e)}")
        
        # Test admin endpoints without authentication (should return 401/403)
        admin_endpoints = [
            ("POST", "/providers", {"name": "Test Provider", "winRate": 80, "tradesLastMonth": 100, "signalTypes": ["Forex"], "subscriptionPrice": 99, "rating": 4.5, "followers": 1000, "description": "Test", "riskLevel": "Medium", "avgPipsProfitMonthly": 300, "affiliateUrl": "https://test.com"}),
            ("POST", "/brokers", {"name": "Test Broker", "accountTypes": ["Standard"], "minDeposit": 100, "maxLeverage": "1:100", "spreadsFrom": 0.1, "rating": 4.0, "regulation": ["FCA"], "instruments": ["Forex"], "platformsSupported": ["MT4"], "withdrawalTime": "24h", "customerSupport": "24/7", "affiliateUrl": "https://test.com"}),
            ("POST", "/testimonials", {"name": "Test User", "role": "Trader", "avatar": "TU", "rating": 5, "text": "Great platform!", "location": "Test City"})
        ]
        
        for method, endpoint, payload in admin_endpoints:
            try:
                if method == "POST":
                    response = await self.client.post(f"{self.base_url}{endpoint}", json=payload)
                
                if response.status_code in [401, 403]:
                    self.log_test(f"{method} {endpoint} (no auth)", True, f"Correctly returned {response.status_code} for unauthenticated admin request")
                else:
                    self.log_test(f"{method} {endpoint} (no auth)", False, f"Expected 401/403, got {response.status_code}")
            except Exception as e:
                self.log_test(f"{method} {endpoint} (no auth)", False, f"Exception: {str(e)}")
    
    async def test_database_seeding(self):
        """Test that database seeding worked correctly"""
        print("=== TESTING DATABASE SEEDING ===")
        
        # Check if we have seed data for each collection
        collections = [
            ("providers", "/providers"),
            ("brokers", "/brokers"), 
            ("testimonials", "/testimonials")
        ]
        
        for collection_name, endpoint in collections:
            try:
                response = await self.client.get(f"{self.base_url}{endpoint}")
                if response.status_code == 200:
                    data = response.json()
                    if "success" in data and data["success"]:
                        count = len(data.get("data", []))
                        total = data.get("total", 0)
                        if count > 0:
                            self.log_test(f"Database seeding: {collection_name}", True, f"Found {count} seeded records (total: {total})")
                        else:
                            self.log_test(f"Database seeding: {collection_name}", False, "No seed data found")
                    else:
                        self.log_test(f"Database seeding: {collection_name}", False, "Invalid response", data)
                else:
                    self.log_test(f"Database seeding: {collection_name}", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"Database seeding: {collection_name}", False, f"Exception: {str(e)}")
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print(f"\nFAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"❌ {result['test']}: {result['details']}")
        
        print("\n" + "="*60)
        
        return passed_tests, failed_tests, total_tests

async def main():
    """Run all backend tests"""
    print("TradingHub Backend API Test Suite")
    print("="*60)
    print(f"Testing backend at: {BACKEND_URL}")
    print("="*60)
    
    async with TradingHubAPITester() as tester:
        # Run all test suites
        await tester.test_health_endpoints()
        await tester.test_database_seeding()
        await tester.test_providers_api()
        await tester.test_brokers_api()
        await tester.test_testimonials_api()
        await tester.test_auth_endpoints()
        
        # Print summary
        passed, failed, total = tester.print_summary()
        
        # Return exit code based on results
        return 0 if failed == 0 else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)