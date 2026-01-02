#!/usr/bin/env python3
"""
Agent 2: The Simulation Agent (The "Imposter")
================================================
Role: Data Generation & QA
Objective: Generate realistic, high-frequency telemetry data that mimics 
           a DJI drone or SpaceX rocket. Floods the system with data to 
           prove the pipes work.

This agent generates telemetry data with:
- 3D coordinates [x, y, z] (longitude, latitude, altitude)
- Timestamp t
- Velocity components
- Device metadata
"""

import json
import time
import random
import math
from datetime import datetime
from kafka import KafkaProducer
from typing import Dict, Tuple


class TelemetrySimulator:
    """Simulates realistic telemetry data for drones and rockets"""
    
    def __init__(self, device_type: str = "drone", device_id: str = None):
        self.device_type = device_type
        self.device_id = device_id or f"{device_type}_{random.randint(1000, 9999)}"
        
        # Initialize position (San Francisco Bay Area)
        # Starting near Golden Gate Bridge
        self.longitude = -122.4194  # X
        self.latitude = 37.8199     # Y
        self.altitude = 50.0        # Z in meters
        
        # Initialize velocity (m/s)
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.velocity_z = 0.0
        
        # Device-specific parameters
        if device_type == "drone":
            self.max_speed = 20.0  # 20 m/s (~45 mph)
            self.max_altitude = 400.0  # 400 meters
            self.battery_level = 100.0
            self.battery_drain_rate = 0.1  # % per second
        else:  # rocket
            self.max_speed = 100.0  # 100 m/s (~220 mph)
            self.max_altitude = 5000.0  # 5 km
            self.battery_level = None
            self.battery_drain_rate = 0
        
        # Random walk parameters
        self.heading = random.uniform(0, 360)  # Initial heading in degrees
        self.turn_rate = 5.0  # degrees per update
        
    def random_walk_step(self, dt: float = 1.0) -> None:
        """
        Perform one step of random walk to simulate realistic movement.
        Uses Brownian motion with momentum for smooth trajectories.
        
        Args:
            dt: Time step in seconds
        """
        # Add random perturbations to heading
        self.heading += random.gauss(0, self.turn_rate)
        self.heading = self.heading % 360
        
        # Calculate target velocity based on heading
        speed = random.uniform(0.5, self.max_speed * 0.7)
        heading_rad = math.radians(self.heading)
        
        target_vx = speed * math.cos(heading_rad) * 0.00001  # Convert to degrees
        target_vy = speed * math.sin(heading_rad) * 0.00001
        target_vz = random.gauss(0, 0.5)  # Vertical velocity (m/s)
        
        # Smooth velocity changes (momentum)
        alpha = 0.3  # Smoothing factor
        self.velocity_x = alpha * target_vx + (1 - alpha) * self.velocity_x
        self.velocity_y = alpha * target_vy + (1 - alpha) * self.velocity_y
        self.velocity_z = alpha * target_vz + (1 - alpha) * self.velocity_z
        
        # Update position
        self.longitude += self.velocity_x * dt
        self.latitude += self.velocity_y * dt
        self.altitude += self.velocity_z * dt
        
        # Boundary constraints
        # Keep within San Francisco Bay Area bounds
        self.longitude = max(-122.6, min(-122.3, self.longitude))
        self.latitude = max(37.6, min(37.9, self.latitude))
        self.altitude = max(0, min(self.max_altitude, self.altitude))
        
        # Drain battery (for drones)
        if self.battery_level is not None:
            self.battery_level = max(0, self.battery_level - self.battery_drain_rate * dt)
    
    def calculate_speed(self) -> float:
        """Calculate current speed in m/s"""
        # Convert velocity from degrees/s to m/s (approximate)
        vx_ms = self.velocity_x * 111320  # 1 degree longitude ≈ 111.32 km at equator
        vy_ms = self.velocity_y * 111320  # 1 degree latitude ≈ 111.32 km
        vz_ms = self.velocity_z
        
        return math.sqrt(vx_ms**2 + vy_ms**2 + vz_ms**2)
    
    def generate_telemetry(self) -> Dict:
        """Generate a single telemetry data packet"""
        timestamp = datetime.utcnow()
        speed = self.calculate_speed()
        
        telemetry = {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "timestamp": timestamp.isoformat() + "Z",
            "coordinates": {
                "longitude": round(self.longitude, 6),  # X
                "latitude": round(self.latitude, 6),    # Y
                "altitude": round(self.altitude, 2)     # Z in meters
            },
            "velocity": {
                "vx": round(self.velocity_x, 8),
                "vy": round(self.velocity_y, 8),
                "vz": round(self.velocity_z, 4)
            },
            "speed": round(speed, 2),
            "heading": round(self.heading, 2),
        }
        
        if self.battery_level is not None:
            telemetry["battery_level"] = round(self.battery_level, 2)
        
        return telemetry


class TelemetryProducer:
    """Kafka producer for streaming telemetry data"""
    
    def __init__(self, bootstrap_servers: str = "localhost:9092", 
                 topic: str = "telemetry_stream"):
        print(f"Initializing Kafka producer...")
        print(f"Bootstrap servers: {bootstrap_servers}")
        print(f"Topic: {topic}")
        
        self.topic = topic
        self.producer = None
        self.connect_to_kafka(bootstrap_servers)
    
    def connect_to_kafka(self, bootstrap_servers: str, max_retries: int = 10) -> None:
        """Connect to Kafka with retry logic"""
        for attempt in range(max_retries):
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=bootstrap_servers,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    acks='all',
                    retries=3
                )
                print(f"✅ Connected to Kafka successfully!")
                return
            except Exception as e:
                print(f"⚠️  Attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise Exception(f"Failed to connect to Kafka after {max_retries} attempts")
    
    def send_telemetry(self, telemetry: Dict) -> None:
        """Send telemetry data to Kafka topic"""
        try:
            future = self.producer.send(self.topic, telemetry)
            # Wait for confirmation (optional, can be removed for higher throughput)
            future.get(timeout=10)
        except Exception as e:
            print(f"❌ Error sending telemetry: {e}")
    
    def close(self) -> None:
        """Close producer connection"""
        if self.producer:
            self.producer.flush()
            self.producer.close()
            print("Producer closed")


def main():
    """Main execution loop"""
    print("=" * 70)
    print("🚁 AGENT 2: THE SIMULATION AGENT (THE IMPOSTER)")
    print("=" * 70)
    print("Role: Data Generation & QA")
    print("Objective: Generate realistic telemetry data to flood the system")
    print("=" * 70)
    
    # Configuration
    DEVICE_TYPE = "drone"  # Change to "rocket" for rocket simulation
    KAFKA_SERVERS = "localhost:9092"
    TOPIC = "telemetry_stream"
    FREQUENCY_HZ = 10  # 10 Hz = 10 messages per second
    
    print(f"\n📊 Simulation Configuration:")
    print(f"   Device Type: {DEVICE_TYPE}")
    print(f"   Kafka Server: {KAFKA_SERVERS}")
    print(f"   Topic: {TOPIC}")
    print(f"   Frequency: {FREQUENCY_HZ} Hz")
    print()
    
    # Initialize simulator and producer
    simulator = TelemetrySimulator(device_type=DEVICE_TYPE)
    producer = TelemetryProducer(bootstrap_servers=KAFKA_SERVERS, topic=TOPIC)
    
    print(f"🚀 Starting telemetry stream for device: {simulator.device_id}")
    print(f"   Initial position: ({simulator.longitude:.4f}, {simulator.latitude:.4f}, {simulator.altitude:.1f}m)")
    print(f"   Press Ctrl+C to stop\n")
    
    message_count = 0
    start_time = time.time()
    
    try:
        while True:
            # Perform random walk step
            simulator.random_walk_step(dt=1.0/FREQUENCY_HZ)
            
            # Generate telemetry packet
            telemetry = simulator.generate_telemetry()
            
            # Send to Kafka
            producer.send_telemetry(telemetry)
            
            # Display progress
            message_count += 1
            if message_count % (FREQUENCY_HZ * 5) == 0:  # Every 5 seconds
                elapsed = time.time() - start_time
                rate = message_count / elapsed
                print(f"📡 Sent {message_count} messages | Rate: {rate:.1f} msg/s | "
                      f"Pos: ({telemetry['coordinates']['longitude']:.4f}, "
                      f"{telemetry['coordinates']['latitude']:.4f}, "
                      f"{telemetry['coordinates']['altitude']:.1f}m) | "
                      f"Speed: {telemetry['speed']:.1f} m/s")
            
            # Sleep to maintain frequency
            time.sleep(1.0 / FREQUENCY_HZ)
            
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Stopping simulation...")
        elapsed = time.time() - start_time
        print(f"📊 Statistics:")
        print(f"   Total messages: {message_count}")
        print(f"   Duration: {elapsed:.1f} seconds")
        print(f"   Average rate: {message_count/elapsed:.1f} msg/s")
    finally:
        producer.close()
        print("✅ Simulation stopped cleanly")


if __name__ == "__main__":
    main()
