-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'resident', 'worker')),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    building_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Buildings table
CREATE TABLE buildings (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    location GEOMETRY(POINT, 4326),
    building_type VARCHAR(50) NOT NULL CHECK (building_type IN ('residential', 'commercial')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Complaints table
CREATE TABLE complaints (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    building_id INTEGER REFERENCES buildings(id),
    category VARCHAR(50) NOT NULL CHECK (category IN ('electricity', 'plumbing', 'sewage', 'maintenance', 'other')),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    location GEOMETRY(POINT, 4326),
    urgency_level VARCHAR(20) NOT NULL CHECK (urgency_level IN ('low', 'medium', 'high', 'critical')),
    status VARCHAR(20) NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'assigned', 'in_progress', 'resolved', 'closed')),
    assigned_worker_id INTEGER REFERENCES users(id),
    image_url VARCHAR(500),
    priority_score FLOAT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

-- Utility consumption table
CREATE TABLE utility_consumption (
    id SERIAL PRIMARY KEY,
    building_id INTEGER REFERENCES buildings(id),
    utility_type VARCHAR(50) NOT NULL CHECK (utility_type IN ('water', 'electricity', 'gas')),
    consumption_value FLOAT NOT NULL,
    unit VARCHAR(20) NOT NULL,
    recorded_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Complaint updates table
CREATE TABLE complaint_updates (
    id SERIAL PRIMARY KEY,
    complaint_id INTEGER REFERENCES complaints(id),
    user_id INTEGER REFERENCES users(id),
    update_text TEXT NOT NULL,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_complaints_location ON complaints USING GIST(location);
CREATE INDEX idx_buildings_location ON buildings USING GIST(location);
CREATE INDEX idx_complaints_status ON complaints(status);
CREATE INDEX idx_complaints_category ON complaints(category);
CREATE INDEX idx_utility_consumption_building_date ON utility_consumption(building_id, recorded_date);
