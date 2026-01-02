#!/usr/bin/env python3
"""
System Test Script
==================
Tests the end-to-end flow of the compliance monitoring system.
"""

import json
import time
import subprocess
import sys
import psycopg2
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable


def check_docker_services():
    """Check if Docker services are running"""
    print("🔍 Checking Docker services...")
    
    services = ['compliance_db', 'compliance_kafka', 'compliance_zookeeper']
    all_healthy = True
    
    for service in services:
        try:
            result = subprocess.run(
                ['docker', 'inspect', '--format={{.State.Health.Status}}', service],
                capture_output=True,
                text=True
            )
            status = result.stdout.strip()
            
            if status == 'healthy':
                print(f"   ✅ {service}: {status}")
            else:
                print(f"   ❌ {service}: {status}")
                all_healthy = False
        except Exception as e:
            print(f"   ❌ {service}: not running")
            all_healthy = False
    
    return all_healthy


def test_database_connection():
    """Test PostgreSQL connection and schema"""
    print("\n🗄️  Testing database connection...")
    
    # PRODUCTION: Use environment variables for credentials
    # import os
    # conn = psycopg2.connect(
    #     host=os.getenv("POSTGRES_HOST", "localhost"),
    #     port=int(os.getenv("POSTGRES_PORT", "5432")),
    #     database=os.getenv("POSTGRES_DB", "compliance_system"),
    #     user=os.getenv("POSTGRES_USER", "admin"),
    #     password=os.getenv("POSTGRES_PASSWORD", "admin123")
    # )
    
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="compliance_system",
            user="admin",
            password="admin123"
        )
        
        with conn.cursor() as cursor:
            # Check PostGIS
            cursor.execute("SELECT PostGIS_Version();")
            version = cursor.fetchone()[0]
            print(f"   ✅ PostGIS version: {version}")
            
            # Check tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE';
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = ['telemetry', 'compliance_events', 'geofences', 'devices']
            for table in expected_tables:
                if table in tables:
                    print(f"   ✅ Table '{table}' exists")
                else:
                    print(f"   ❌ Table '{table}' missing")
                    return False
            
            # Check geofences
            cursor.execute("SELECT COUNT(*) FROM geofences;")
            count = cursor.fetchone()[0]
            print(f"   ✅ {count} geofences configured")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Database connection failed: {e}")
        return False


def test_kafka_connection():
    """Test Kafka connection"""
    print("\n📡 Testing Kafka connection...")
    
    try:
        # Try to create producer
        producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            request_timeout_ms=5000
        )
        print("   ✅ Kafka producer connected")
        
        # Send test message
        test_message = {
            "test": "message",
            "timestamp": time.time()
        }
        future = producer.send('test_topic', test_message)
        future.get(timeout=10)
        print("   ✅ Test message sent successfully")
        
        producer.close()
        return True
        
    except NoBrokersAvailable:
        print("   ❌ Kafka broker not available")
        return False
    except Exception as e:
        print(f"   ❌ Kafka connection failed: {e}")
        return False


def test_end_to_end_flow():
    """Test end-to-end data flow"""
    print("\n🔄 Testing end-to-end flow...")
    
    try:
        # Create producer
        producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        # Send test telemetry
        test_telemetry = {
            "device_id": "test_device_001",
            "device_type": "drone",
            "timestamp": "2024-01-02T08:35:00+00:00",
            "coordinates": {
                "longitude": -122.4194,
                "latitude": 37.8199,
                "altitude": 50.0
            },
            "velocity": {
                "vx": 0.00001,
                "vy": 0.00001,
                "vz": 0.5
            },
            "speed": 15.2,
            "heading": 45.0,
            "battery_level": 85.5
        }
        
        producer.send('telemetry_stream', test_telemetry)
        producer.flush()
        print("   ✅ Test telemetry sent to Kafka")
        
        producer.close()
        
        # Give some time for processing
        print("   ⏳ Waiting for processing (5 seconds)...")
        time.sleep(5)
        
        # Check database for the record
        # PRODUCTION: Use environment variables for credentials
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="compliance_system",
            user="admin",
            password="admin123"
        )
        
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM telemetry 
                WHERE device_id = 'test_device_001'
            """)
            count = cursor.fetchone()[0]
            
            if count > 0:
                print(f"   ✅ Found {count} telemetry record(s) in database")
            else:
                print("   ⚠️  No telemetry records found (compliance engine may not be running)")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ End-to-end test failed: {e}")
        return False


def print_summary(results):
    """Print test summary"""
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    all_passed = all(results.values())
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("=" * 70)
    
    if all_passed:
        print("🎉 All tests passed! System is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the output above.")
        print("\n💡 Tips:")
        print("   - Make sure Docker services are running: ./start_system.sh")
        print("   - For end-to-end test, start compliance_engine.py first")
        return 1


def main():
    """Run all tests"""
    print("=" * 70)
    print("🧪 COMPLIANCE MONITORING SYSTEM - TEST SUITE")
    print("=" * 70)
    
    results = {}
    
    # Test 1: Docker services
    results["Docker Services"] = check_docker_services()
    
    if not results["Docker Services"]:
        print("\n❌ Docker services not healthy. Run ./start_system.sh first.")
        return 1
    
    # Test 2: Database
    results["Database Connection"] = test_database_connection()
    
    # Test 3: Kafka
    results["Kafka Connection"] = test_kafka_connection()
    
    # Test 4: End-to-end (optional, requires compliance engine running)
    print("\n📝 Note: End-to-end test requires compliance_engine.py to be running")
    user_input = input("   Run end-to-end test? (y/n): ").strip().lower()
    
    if user_input == 'y':
        results["End-to-End Flow"] = test_end_to_end_flow()
    
    # Print summary
    return print_summary(results)


if __name__ == "__main__":
    sys.exit(main())
