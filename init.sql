-- Initialize PostGIS Extension for Spatial Operations
CREATE EXTENSION IF NOT EXISTS postgis;

-- Telemetry Table: Store all incoming data points
-- This is the permanent, unalterable ledger for every ping
CREATE TABLE IF NOT EXISTS telemetry (
    id BIGSERIAL PRIMARY KEY,
    device_id VARCHAR(100) NOT NULL,
    device_type VARCHAR(50) NOT NULL, -- 'drone' or 'rocket'
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    location GEOMETRY(PointZ, 4326) NOT NULL, -- 3D point (longitude, latitude, altitude)
    velocity_x DOUBLE PRECISION,
    velocity_y DOUBLE PRECISION,
    velocity_z DOUBLE PRECISION,
    speed DOUBLE PRECISION, -- Calculated speed in m/s
    heading DOUBLE PRECISION, -- Direction in degrees
    battery_level DOUBLE PRECISION, -- Battery percentage (for drones)
    raw_data JSONB, -- Store original JSON payload
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Compliance Events Table: Store violations and compliance checks
CREATE TABLE IF NOT EXISTS compliance_events (
    id BIGSERIAL PRIMARY KEY,
    telemetry_id BIGINT REFERENCES telemetry(id),
    device_id VARCHAR(100) NOT NULL,
    event_type VARCHAR(50) NOT NULL, -- 'COMPLIANT', 'VIOLATION', 'WARNING'
    rule_violated VARCHAR(100), -- e.g., 'GEOFENCE_EXIT', 'SPEED_LIMIT', 'NO_FLY_ZONE'
    severity VARCHAR(20), -- 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    location GEOMETRY(PointZ, 4326) NOT NULL,
    details JSONB, -- Additional context about the event
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Geofence Definitions: Define allowed/restricted zones
CREATE TABLE IF NOT EXISTS geofences (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    fence_type VARCHAR(50) NOT NULL, -- 'ALLOWED', 'NO_FLY', 'RESTRICTED'
    boundary GEOMETRY(Polygon, 4326) NOT NULL, -- 2D polygon boundary
    min_altitude DOUBLE PRECISION, -- Minimum altitude in meters
    max_altitude DOUBLE PRECISION, -- Maximum altitude in meters
    max_speed DOUBLE PRECISION, -- Speed limit in m/s
    active BOOLEAN DEFAULT TRUE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Devices Registry: Track registered devices
CREATE TABLE IF NOT EXISTS devices (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(100) UNIQUE NOT NULL,
    device_type VARCHAR(50) NOT NULL,
    owner VARCHAR(200),
    registration_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    active BOOLEAN DEFAULT TRUE,
    metadata JSONB
);

-- Create Spatial Indexes (R-Tree) for efficient spatial queries
CREATE INDEX IF NOT EXISTS idx_telemetry_location ON telemetry USING GIST (location);
CREATE INDEX IF NOT EXISTS idx_telemetry_timestamp ON telemetry (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_telemetry_device ON telemetry (device_id, timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_compliance_location ON compliance_events USING GIST (location);
CREATE INDEX IF NOT EXISTS idx_compliance_timestamp ON compliance_events (detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_compliance_device ON compliance_events (device_id, detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_compliance_event_type ON compliance_events (event_type, severity);

CREATE INDEX IF NOT EXISTS idx_geofences_boundary ON geofences USING GIST (boundary);
CREATE INDEX IF NOT EXISTS idx_geofences_active ON geofences (active) WHERE active = TRUE;

-- Insert sample geofences for testing
-- Geofence 1: Allowed flight zone (San Francisco Bay Area)
INSERT INTO geofences (name, fence_type, boundary, min_altitude, max_altitude, max_speed, description)
VALUES (
    'SF Bay Allowed Zone',
    'ALLOWED',
    ST_GeomFromText('POLYGON((-122.5 37.7, -122.3 37.7, -122.3 37.9, -122.5 37.9, -122.5 37.7))', 4326),
    0,
    400, -- 400 meters max altitude (~1300 feet)
    30, -- 30 m/s max speed (~67 mph)
    'General allowed flight zone in San Francisco Bay Area'
);

-- Geofence 2: No-fly zone (Airport)
INSERT INTO geofences (name, fence_type, boundary, min_altitude, max_altitude, max_speed, description)
VALUES (
    'SFO Airport No-Fly Zone',
    'NO_FLY',
    ST_GeomFromText('POLYGON((-122.4 37.6, -122.35 37.6, -122.35 37.65, -122.4 37.65, -122.4 37.6))', 4326),
    0,
    10000, -- Complete no-fly at all altitudes
    NULL,
    'San Francisco International Airport restricted airspace'
);

-- Geofence 3: Restricted zone (Downtown - limited altitude)
INSERT INTO geofences (name, fence_type, boundary, min_altitude, max_altitude, max_speed, description)
VALUES (
    'Downtown SF Restricted',
    'RESTRICTED',
    ST_GeomFromText('POLYGON((-122.42 37.78, -122.38 37.78, -122.38 37.82, -122.42 37.82, -122.42 37.78))', 4326),
    0,
    120, -- 120 meters max altitude (~400 feet)
    15, -- 15 m/s max speed (~34 mph)
    'Downtown San Francisco - restricted altitude and speed'
);

-- Create a view for easy compliance checking
CREATE OR REPLACE VIEW telemetry_with_compliance AS
SELECT 
    t.id,
    t.device_id,
    t.device_type,
    t.timestamp,
    ST_X(t.location) as longitude,
    ST_Y(t.location) as latitude,
    ST_Z(t.location) as altitude,
    t.speed,
    t.heading,
    COALESCE(ce.event_type, 'COMPLIANT') as compliance_status,
    ce.rule_violated,
    ce.severity
FROM telemetry t
LEFT JOIN compliance_events ce ON t.id = ce.telemetry_id
ORDER BY t.timestamp DESC;

-- Function to calculate distance between two 3D points
CREATE OR REPLACE FUNCTION calculate_3d_distance(
    point1 GEOMETRY,
    point2 GEOMETRY
) RETURNS DOUBLE PRECISION AS $$
BEGIN
    RETURN ST_3DDistance(point1, point2);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function to check if point is within geofence
CREATE OR REPLACE FUNCTION check_geofence_violation(
    device_location GEOMETRY,
    device_speed DOUBLE PRECISION
) RETURNS TABLE(
    is_violation BOOLEAN,
    fence_name VARCHAR,
    fence_type VARCHAR,
    rule_violated VARCHAR,
    severity VARCHAR
) AS $$
BEGIN
    -- Check NO_FLY zones
    RETURN QUERY
    SELECT 
        TRUE as is_violation,
        g.name,
        g.fence_type,
        'NO_FLY_ZONE' as rule_violated,
        'CRITICAL' as severity
    FROM geofences g
    WHERE g.active = TRUE
        AND g.fence_type = 'NO_FLY'
        AND ST_Within(ST_MakePoint(ST_X(device_location), ST_Y(device_location)), g.boundary)
        AND ST_Z(device_location) BETWEEN COALESCE(g.min_altitude, 0) AND COALESCE(g.max_altitude, 10000)
    LIMIT 1;
    
    -- If in NO_FLY zone, return immediately
    IF FOUND THEN
        RETURN;
    END IF;
    
    -- Check RESTRICTED zones for altitude and speed violations
    RETURN QUERY
    SELECT 
        TRUE as is_violation,
        g.name,
        g.fence_type,
        CASE 
            WHEN ST_Z(device_location) > g.max_altitude THEN 'ALTITUDE_VIOLATION'
            WHEN device_speed > g.max_speed THEN 'SPEED_VIOLATION'
            ELSE 'RESTRICTED_ZONE'
        END as rule_violated,
        'HIGH' as severity
    FROM geofences g
    WHERE g.active = TRUE
        AND g.fence_type = 'RESTRICTED'
        AND ST_Within(ST_MakePoint(ST_X(device_location), ST_Y(device_location)), g.boundary)
        AND (
            ST_Z(device_location) > COALESCE(g.max_altitude, 10000)
            OR device_speed > COALESCE(g.max_speed, 1000)
        )
    LIMIT 1;
    
    -- If no violations found, return FALSE
    IF NOT FOUND THEN
        RETURN QUERY
        SELECT FALSE, NULL::VARCHAR, NULL::VARCHAR, NULL::VARCHAR, NULL::VARCHAR;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Grant permissions (for security, adjust in production)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO admin;
