#!/usr/bin/env python3
"""
Agent 3: The Compliance Auditor (The "Product") 
Agent 4: The Archivist (The Database Admin)
================================================
Agent 3 Role: Core Logic & Verification
Agent 3 Objective: Watch data stream in real-time, hold rules, judge 
                   every packet: Compliant or Violation

Agent 4 Role: Data Persistence & Ledger
Agent 4 Objective: Ensure every single ping is written to permanent, 
                   unalterable SQL ledger

This engine combines both agents:
- Consumes telemetry from Kafka (Agent 3)
- Checks compliance rules using PostGIS (Agent 3)
- Writes all data to PostgreSQL ledger (Agent 4)
"""

import json
import time
import signal
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from kafka import KafkaConsumer
import psycopg2
from psycopg2.extras import execute_values


class ComplianceRules:
    """Define and check compliance rules"""
    
    # Speed limits (m/s)
    DRONE_MAX_SPEED = 30.0  # ~67 mph
    ROCKET_MAX_SPEED = 100.0  # ~220 mph
    
    # Altitude limits (meters)
    GENERAL_MAX_ALTITUDE = 400.0  # ~1300 feet
    RESTRICTED_MAX_ALTITUDE = 120.0  # ~400 feet
    
    @staticmethod
    def check_speed_violation(speed: float, device_type: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """Check if speed exceeds limits"""
        max_speed = ComplianceRules.DRONE_MAX_SPEED if device_type == "drone" else ComplianceRules.ROCKET_MAX_SPEED
        
        if speed > max_speed:
            return True, "SPEED_LIMIT", "HIGH"
        return False, None, None
    
    @staticmethod
    def check_altitude_violation(altitude: float, device_type: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """Check if altitude exceeds limits"""
        if altitude > ComplianceRules.GENERAL_MAX_ALTITUDE:
            return True, "ALTITUDE_VIOLATION", "MEDIUM"
        return False, None, None
    
    @staticmethod
    def check_battery_warning(battery_level: Optional[float]) -> Tuple[bool, Optional[str], Optional[str]]:
        """Check if battery is critically low"""
        if battery_level is not None and battery_level < 20.0:
            severity = "CRITICAL" if battery_level < 10.0 else "MEDIUM"
            return True, "LOW_BATTERY", severity
        return False, None, None


class DatabaseArchive:
    """Agent 4: The Archivist - Manages PostgreSQL ledger"""
    
    def __init__(self, db_config: Dict):
        self.db_config = db_config
        self.connection = None
        self.connect()
    
    def connect(self, max_retries: int = 10) -> None:
        """Connect to PostgreSQL with retry logic"""
        print("🗄️  Connecting to PostgreSQL database...")
        
        for attempt in range(max_retries):
            try:
                self.connection = psycopg2.connect(**self.db_config)
                self.connection.autocommit = False
                print("✅ Connected to database successfully!")
                
                # Verify PostGIS is available
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT PostGIS_Version();")
                    version = cursor.fetchone()
                    print(f"   PostGIS Version: {version[0]}")
                
                return
            except Exception as e:
                print(f"⚠️  Attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"   Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise Exception(f"Failed to connect to database after {max_retries} attempts")
    
    def store_telemetry(self, telemetry: Dict) -> int:
        """
        Store telemetry data in permanent ledger
        Returns the telemetry_id for reference
        """
        try:
            with self.connection.cursor() as cursor:
                # Parse telemetry data
                device_id = telemetry["device_id"]
                device_type = telemetry["device_type"]
                timestamp = telemetry["timestamp"]
                
                coords = telemetry["coordinates"]
                longitude = coords["longitude"]
                latitude = coords["latitude"]
                altitude = coords["altitude"]
                
                velocity = telemetry["velocity"]
                velocity_x = velocity["vx"]
                velocity_y = velocity["vy"]
                velocity_z = velocity["vz"]
                
                speed = telemetry["speed"]
                heading = telemetry["heading"]
                battery_level = telemetry.get("battery_level")
                
                # Insert into telemetry table with 3D point
                insert_query = """
                    INSERT INTO telemetry (
                        device_id, device_type, timestamp, location,
                        velocity_x, velocity_y, velocity_z, speed, heading,
                        battery_level, raw_data
                    ) VALUES (
                        %s, %s, %s, ST_GeomFromText(%s, 4326),
                        %s, %s, %s, %s, %s, %s, %s
                    ) RETURNING id;
                """
                
                # Create 3D point (POINT Z)
                point_wkt = f"POINT Z ({longitude} {latitude} {altitude})"
                
                cursor.execute(insert_query, (
                    device_id, device_type, timestamp, point_wkt,
                    velocity_x, velocity_y, velocity_z, speed, heading,
                    battery_level, json.dumps(telemetry)
                ))
                
                telemetry_id = cursor.fetchone()[0]
                self.connection.commit()
                
                return telemetry_id
                
        except Exception as e:
            self.connection.rollback()
            print(f"❌ Error storing telemetry: {e}")
            raise
    
    def store_compliance_event(self, telemetry_id: int, telemetry: Dict,
                               event_type: str, rule_violated: Optional[str],
                               severity: Optional[str], details: Dict) -> None:
        """Store compliance event (violation or warning)"""
        try:
            with self.connection.cursor() as cursor:
                coords = telemetry["coordinates"]
                longitude = coords["longitude"]
                latitude = coords["latitude"]
                altitude = coords["altitude"]
                point_wkt = f"POINT Z ({longitude} {latitude} {altitude})"
                
                insert_query = """
                    INSERT INTO compliance_events (
                        telemetry_id, device_id, event_type, rule_violated,
                        severity, location, details
                    ) VALUES (
                        %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326), %s
                    );
                """
                
                cursor.execute(insert_query, (
                    telemetry_id, telemetry["device_id"], event_type,
                    rule_violated, severity, point_wkt, json.dumps(details)
                ))
                
                self.connection.commit()
                
        except Exception as e:
            self.connection.rollback()
            print(f"❌ Error storing compliance event: {e}")
            raise
    
    def check_geofence_violations(self, telemetry_id: int, longitude: float,
                                   latitude: float, altitude: float, speed: float) -> List[Dict]:
        """Use PostGIS to check geofence violations"""
        try:
            with self.connection.cursor() as cursor:
                point_wkt = f"POINT Z ({longitude} {latitude} {altitude})"
                
                query = """
                    SELECT * FROM check_geofence_violation(
                        ST_GeomFromText(%s, 4326), %s
                    );
                """
                
                cursor.execute(query, (point_wkt, speed))
                results = cursor.fetchall()
                
                violations = []
                for row in results:
                    is_violation, fence_name, fence_type, rule_violated, severity = row
                    if is_violation:
                        violations.append({
                            "fence_name": fence_name,
                            "fence_type": fence_type,
                            "rule_violated": rule_violated,
                            "severity": severity
                        })
                
                return violations
                
        except Exception as e:
            print(f"❌ Error checking geofence: {e}")
            return []
    
    def close(self) -> None:
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("Database connection closed")


class ComplianceEngine:
    """Agent 3: The Compliance Auditor - Core logic and verification"""
    
    def __init__(self, kafka_config: Dict, db_config: Dict):
        print("=" * 70)
        print("🔍 AGENT 3: THE COMPLIANCE AUDITOR (THE PRODUCT)")
        print("🗄️  AGENT 4: THE ARCHIVIST (THE DATABASE ADMIN)")
        print("=" * 70)
        print("Agent 3 Role: Core Logic & Verification")
        print("Agent 4 Role: Data Persistence & Ledger")
        print("=" * 70)
        
        self.kafka_config = kafka_config
        self.db_archive = DatabaseArchive(db_config)
        self.consumer = None
        self.stats = {
            "total_processed": 0,
            "compliant": 0,
            "violations": 0,
            "warnings": 0
        }
        
        # Setup graceful shutdown
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        
        self.running = True
    
    def connect_to_kafka(self) -> None:
        """Connect to Kafka consumer"""
        print("\n📡 Connecting to Kafka...")
        
        max_retries = 10
        for attempt in range(max_retries):
            try:
                self.consumer = KafkaConsumer(
                    self.kafka_config["topic"],
                    bootstrap_servers=self.kafka_config["bootstrap_servers"],
                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                    auto_offset_reset='latest',
                    enable_auto_commit=True,
                    group_id='compliance_engine_group'
                )
                print("✅ Connected to Kafka successfully!")
                return
            except Exception as e:
                print(f"⚠️  Attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"   Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise Exception(f"Failed to connect to Kafka after {max_retries} attempts")
    
    def audit_telemetry(self, telemetry: Dict, telemetry_id: int) -> Tuple[str, List[Dict]]:
        """
        Agent 3: Audit telemetry for compliance
        Returns: (event_type, violations_list)
        """
        violations = []
        device_type = telemetry["device_type"]
        speed = telemetry["speed"]
        altitude = telemetry["coordinates"]["altitude"]
        battery_level = telemetry.get("battery_level")
        
        # Check speed violations
        is_violation, rule, severity = ComplianceRules.check_speed_violation(speed, device_type)
        if is_violation:
            violations.append({"rule": rule, "severity": severity, "value": speed})
        
        # Check altitude violations
        is_violation, rule, severity = ComplianceRules.check_altitude_violation(altitude, device_type)
        if is_violation:
            violations.append({"rule": rule, "severity": severity, "value": altitude})
        
        # Check battery warnings
        is_warning, rule, severity = ComplianceRules.check_battery_warning(battery_level)
        if is_warning:
            violations.append({"rule": rule, "severity": severity, "value": battery_level})
        
        # Check geofence violations using PostGIS
        coords = telemetry["coordinates"]
        geofence_violations = self.db_archive.check_geofence_violations(
            telemetry_id, coords["longitude"], coords["latitude"],
            coords["altitude"], speed
        )
        
        for gv in geofence_violations:
            violations.append({
                "rule": gv["rule_violated"],
                "severity": gv["severity"],
                "fence_name": gv["fence_name"],
                "fence_type": gv["fence_type"]
            })
        
        # Determine overall event type
        if not violations:
            return "COMPLIANT", []
        
        has_critical = any(v["severity"] == "CRITICAL" for v in violations)
        has_high = any(v["severity"] == "HIGH" for v in violations)
        
        if has_critical or has_high:
            return "VIOLATION", violations
        else:
            return "WARNING", violations
    
    def process_message(self, telemetry: Dict) -> None:
        """Process a single telemetry message"""
        try:
            # Agent 4: Archive to permanent ledger
            telemetry_id = self.db_archive.store_telemetry(telemetry)
            
            # Agent 3: Audit for compliance
            event_type, violations = self.audit_telemetry(telemetry, telemetry_id)
            
            # Update statistics
            self.stats["total_processed"] += 1
            if event_type == "COMPLIANT":
                self.stats["compliant"] += 1
            elif event_type == "VIOLATION":
                self.stats["violations"] += 1
            else:
                self.stats["warnings"] += 1
            
            # Store compliance events
            if violations:
                for violation in violations:
                    self.db_archive.store_compliance_event(
                        telemetry_id, telemetry, event_type,
                        violation["rule"], violation["severity"],
                        violation
                    )
            
            # Log significant events
            if event_type != "COMPLIANT":
                emoji = "🚨" if event_type == "VIOLATION" else "⚠️ "
                coords = telemetry["coordinates"]
                print(f"{emoji} {event_type} detected for {telemetry['device_id']} "
                      f"at ({coords['longitude']:.4f}, {coords['latitude']:.4f}, {coords['altitude']:.1f}m)")
                for v in violations:
                    print(f"   └─ {v['rule']} [{v['severity']}]")
            
            # Periodic status updates
            if self.stats["total_processed"] % 50 == 0:
                self.print_stats()
                
        except Exception as e:
            print(f"❌ Error processing message: {e}")
    
    def print_stats(self) -> None:
        """Print current statistics"""
        total = self.stats["total_processed"]
        compliant_pct = (self.stats["compliant"] / total * 100) if total > 0 else 0
        violation_pct = (self.stats["violations"] / total * 100) if total > 0 else 0
        warning_pct = (self.stats["warnings"] / total * 100) if total > 0 else 0
        
        print(f"\n📊 Statistics (Total: {total})")
        print(f"   ✅ Compliant: {self.stats['compliant']} ({compliant_pct:.1f}%)")
        print(f"   🚨 Violations: {self.stats['violations']} ({violation_pct:.1f}%)")
        print(f"   ⚠️  Warnings: {self.stats['warnings']} ({warning_pct:.1f}%)\n")
    
    def run(self) -> None:
        """Main processing loop"""
        self.connect_to_kafka()
        
        print(f"\n🚀 Starting compliance engine...")
        print(f"   Kafka Topic: {self.kafka_config['topic']}")
        print(f"   Listening for telemetry data...")
        print(f"   Press Ctrl+C to stop\n")
        
        try:
            for message in self.consumer:
                if not self.running:
                    break
                
                telemetry = message.value
                self.process_message(telemetry)
                
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
        finally:
            self.cleanup()
    
    def shutdown(self, signum, frame) -> None:
        """Graceful shutdown handler"""
        print(f"\n\n⏹️  Received shutdown signal...")
        self.running = False
    
    def cleanup(self) -> None:
        """Clean up resources"""
        print("\n🧹 Cleaning up resources...")
        
        if self.consumer:
            self.consumer.close()
            print("   Kafka consumer closed")
        
        self.db_archive.close()
        
        self.print_stats()
        print("\n✅ Compliance engine stopped cleanly")


def main():
    """Main execution"""
    # Kafka configuration
    kafka_config = {
        "bootstrap_servers": "localhost:9092",
        "topic": "telemetry_stream"
    }
    
    # Database configuration
    db_config = {
        "host": "localhost",
        "port": 5432,
        "database": "compliance_system",
        "user": "admin",
        "password": "admin123"
    }
    
    # Initialize and run compliance engine
    engine = ComplianceEngine(kafka_config, db_config)
    engine.run()


if __name__ == "__main__":
    main()
