# 🚁 Compliance Monitoring System for Drones & Rockets

A real-time compliance monitoring system that tracks telemetry data from drones and rockets, verifies compliance with airspace regulations, and maintains a permanent audit ledger.

## 🏗️ Architecture: The 4 Agents

This system implements a **4-agent architecture** where each agent has a specific role:

### 1️⃣ **Agent Zero: The Infrastructure Architect**
**Role:** DevOps & Foundation  
**Objective:** Build the containerized environment where all other agents live  
**Tools:** Docker Compose, PostgreSQL (PostGIS), Apache Kafka, Zookeeper  
**Output:** `docker-compose.yml` - Spins up the entire digital universe in one command

### 2️⃣ **Agent 2: The Simulation Agent (The "Imposter")**
**Role:** Data Generation & QA  
**Objective:** Generate realistic, high-frequency telemetry data mimicking DJI drones or SpaceX rockets  
**Tools:** Python, Random Walk Algorithms, JSON Serializer  
**Output:** `producer.py` - Streams coordinates `[x, y, z, t]` into the system

### 3️⃣ **Agent 3: The Compliance Auditor (The "Product")**
**Role:** Core Logic & Verification  
**Objective:** Watch data stream in real-time and judge every packet: Compliant or Violation  
**Tools:** Python, Kafka Consumer, PostGIS Spatial Queries  
**Output:** `compliance_engine.py` - Filters noise and flags violations

### 4️⃣ **Agent 4: The Archivist (The Database Admin)**
**Role:** Data Persistence & Ledger  
**Objective:** Ensure every ping is written to a permanent, unalterable SQL ledger  
**Tools:** SQL, Spatial Indexing (R-Tree)  
**Output:** `init.sql` - Schema for storing 3D points in a 2D database

## 🔄 Workflow Summary

```
┌─────────────────────────────────────────────────────────────┐
│  Architect builds the house (Docker containers)              │
│         ↓                                                    │
│  Simulator throws balls into the house (telemetry data)     │
│         ↓                                                    │
│  Auditor catches the balls and checks color (compliance)    │
│         ↓                                                    │
│  Archivist puts the balls in closet (permanent storage)     │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.8+
- 4GB RAM minimum

### 1. Start the Infrastructure (Agent Zero)

```bash
# Clone the repository
git clone https://github.com/why-tf-knot/AI-Poster.git
cd AI-Poster

# Start all services (PostgreSQL, Kafka, Zookeeper)
docker-compose up -d

# Wait for services to be healthy (30-60 seconds)
docker-compose ps
```

Expected output:
```
NAME                    STATUS              PORTS
compliance_db           Up (healthy)        5432
compliance_kafka        Up (healthy)        9092, 9093
compliance_zookeeper    Up (healthy)        2181
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Compliance Engine (Agents 3 & 4)

```bash
# In terminal 1
python compliance_engine.py
```

Expected output:
```
🔍 AGENT 3: THE COMPLIANCE AUDITOR (THE PRODUCT)
🗄️  AGENT 4: THE ARCHIVIST (THE DATABASE ADMIN)
✅ Connected to database successfully!
✅ Connected to Kafka successfully!
🚀 Starting compliance engine...
```

### 4. Start the Telemetry Simulator (Agent 2)

```bash
# In terminal 2
python producer.py
```

Expected output:
```
🚁 AGENT 2: THE SIMULATION AGENT (THE IMPOSTER)
✅ Connected to Kafka successfully!
🚀 Starting telemetry stream for device: drone_1234
📡 Sent 50 messages | Rate: 10.0 msg/s | Pos: (-122.4194, 37.8199, 50.0m)
```

## 📊 System Components

### Database Schema (Agent 4)

The system uses PostgreSQL with PostGIS extension for spatial operations:

#### **telemetry** table
Stores all incoming telemetry data with 3D coordinates:
- `id`: Unique identifier
- `device_id`: Device identifier (e.g., "drone_1234")
- `device_type`: "drone" or "rocket"
- `location`: PostGIS POINT Z geometry (lon, lat, altitude)
- `velocity_x`, `velocity_y`, `velocity_z`: Velocity components
- `speed`: Calculated speed in m/s
- `heading`: Direction in degrees
- `battery_level`: Battery percentage (drones only)
- `raw_data`: Original JSON payload

#### **compliance_events** table
Stores violations and compliance checks:
- `id`: Unique identifier
- `telemetry_id`: Reference to telemetry record
- `event_type`: "COMPLIANT", "VIOLATION", or "WARNING"
- `rule_violated`: Type of violation (e.g., "SPEED_LIMIT", "NO_FLY_ZONE")
- `severity`: "LOW", "MEDIUM", "HIGH", or "CRITICAL"

#### **geofences** table
Defines allowed/restricted zones:
- `boundary`: PostGIS Polygon for 2D boundary
- `fence_type`: "ALLOWED", "NO_FLY", or "RESTRICTED"
- `min_altitude`, `max_altitude`: Altitude constraints
- `max_speed`: Speed limit in m/s

### Compliance Rules (Agent 3)

The system enforces the following rules:

1. **Speed Limits**
   - Drones: Max 30 m/s (~67 mph)
   - Rockets: Max 100 m/s (~220 mph)

2. **Altitude Limits**
   - General: Max 400m (~1300 feet)
   - Restricted zones: Max 120m (~400 feet)

3. **Geofence Rules**
   - NO_FLY zones: Complete prohibition
   - RESTRICTED zones: Altitude/speed limits
   - ALLOWED zones: Normal operations

4. **Battery Warnings**
   - Warning: <20% battery
   - Critical: <10% battery

### Telemetry Data Format

```json
{
  "device_id": "drone_1234",
  "device_type": "drone",
  "timestamp": "2024-01-02T08:35:00.000Z",
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
```

## 🔍 Monitoring & Verification

### Check Database Records

```bash
# Connect to PostgreSQL
docker exec -it compliance_db psql -U admin -d compliance_system

# Query recent telemetry
SELECT device_id, timestamp, ST_AsText(location), speed 
FROM telemetry 
ORDER BY timestamp DESC 
LIMIT 10;

# Query violations
SELECT device_id, event_type, rule_violated, severity, detected_at
FROM compliance_events
WHERE event_type = 'VIOLATION'
ORDER BY detected_at DESC
LIMIT 10;

# Query compliance summary
SELECT 
    event_type,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM compliance_events
GROUP BY event_type;
```

### Check Kafka Topics

```bash
# List topics
docker exec -it compliance_kafka kafka-topics --bootstrap-server localhost:9092 --list

# Consume messages
docker exec -it compliance_kafka kafka-console-consumer \
    --bootstrap-server localhost:9092 \
    --topic telemetry_stream \
    --from-beginning
```

## 🛠️ Configuration

### Change Device Type

Edit `producer.py` line 280:
```python
DEVICE_TYPE = "rocket"  # Change to "rocket" for rocket simulation
```

### Change Frequency

Edit `producer.py` line 283:
```python
FREQUENCY_HZ = 20  # Increase to 20 Hz for higher throughput
```

### Add Custom Geofences

```sql
INSERT INTO geofences (name, fence_type, boundary, min_altitude, max_altitude, max_speed, description)
VALUES (
    'Custom No-Fly Zone',
    'NO_FLY',
    ST_GeomFromText('POLYGON((-122.5 37.7, -122.4 37.7, -122.4 37.8, -122.5 37.8, -122.5 37.7))', 4326),
    0,
    10000,
    NULL,
    'Custom restricted airspace'
);
```

## 📈 Performance

- **Throughput**: 10-100 messages/second per producer
- **Latency**: <100ms end-to-end (producer → Kafka → consumer → database)
- **Storage**: ~500 bytes per telemetry record
- **Scalability**: Horizontal scaling via Kafka consumer groups

## 🔒 Security Considerations

⚠️ **This is a development setup. For production:**

1. Change default passwords in `docker-compose.yml`
2. Use environment variables for sensitive data
3. Enable SSL/TLS for Kafka connections
4. Implement authentication and authorization
5. Set up database backups
6. Use read-only database replicas for queries
7. Implement rate limiting

## 🧪 Testing

### Generate Violations

Modify `producer.py` to force violations:

```python
# Force altitude violation
self.altitude = 500.0  # Exceeds 400m limit

# Force speed violation
self.max_speed = 50.0  # Exceeds 30 m/s limit
```

### Simulate Multiple Devices

```bash
# Terminal 1
python producer.py  # Device 1

# Terminal 2
python producer.py  # Device 2 (auto-generates new device_id)
```

## 📖 API Reference

### Producer API

```python
from producer import TelemetrySimulator, TelemetryProducer

# Create simulator
simulator = TelemetrySimulator(device_type="drone", device_id="test_001")

# Generate telemetry
telemetry = simulator.generate_telemetry()

# Send to Kafka
producer = TelemetryProducer(bootstrap_servers="localhost:9092")
producer.send_telemetry(telemetry)
```

### Compliance Engine API

```python
from compliance_engine import ComplianceEngine

# Configure
kafka_config = {"bootstrap_servers": "localhost:9092", "topic": "telemetry_stream"}
db_config = {"host": "localhost", "database": "compliance_system", ...}

# Run
engine = ComplianceEngine(kafka_config, db_config)
engine.run()
```

## 🛑 Stopping the System

```bash
# Stop Python scripts
Ctrl+C in each terminal

# Stop Docker containers
docker-compose down

# Stop and remove all data
docker-compose down -v
```

## 🐛 Troubleshooting

### Kafka Connection Failed
```bash
# Check Kafka is running
docker logs compliance_kafka

# Wait for Kafka to be ready (may take 30-60 seconds)
docker-compose ps
```

### Database Connection Failed
```bash
# Check PostgreSQL is running
docker logs compliance_db

# Verify PostGIS extension
docker exec -it compliance_db psql -U admin -d compliance_system -c "SELECT PostGIS_Version();"
```

### No Messages Received
```bash
# Check Kafka topic exists
docker exec -it compliance_kafka kafka-topics --bootstrap-server localhost:9092 --list

# Check consumer group
docker exec -it compliance_kafka kafka-consumer-groups --bootstrap-server localhost:9092 --list
```

## 📚 Additional Resources

- [PostGIS Documentation](https://postgis.net/documentation/)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [FAA Drone Regulations](https://www.faa.gov/uas)
- [Geofencing Best Practices](https://www.faa.gov/uas/recreational_flyers)

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Machine learning for anomaly detection
- Real-time visualization dashboard
- Multi-region support
- Advanced trajectory prediction
- Integration with real drone APIs (DJI, ArduPilot)

## 📜 License

MIT License - See LICENSE file for details

## 👏 Acknowledgments

Built with:
- PostgreSQL + PostGIS for spatial operations
- Apache Kafka for message streaming
- Python + kafka-python for producers/consumers
- Docker for containerization

---

**🌌 "The system is the truth. The ledger never lies." 🌌**
