-- Insert sample buildings
INSERT INTO buildings (name, address, location, building_type) VALUES
('Sunrise Apartments', '123 Main St, City', ST_GeomFromText('POINT(77.2090 28.6139)', 4326), 'residential'),
('Tech Plaza', '456 Business Ave, City', ST_GeomFromText('POINT(77.2100 28.6150)', 4326), 'commercial'),
('Green Valley Society', '789 Garden Road, City', ST_GeomFromText('POINT(77.2080 28.6120)', 4326), 'residential');

-- Insert sample users
INSERT INTO users (email, password_hash, role, first_name, last_name, phone, building_id) VALUES
('admin@system.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdXdZSk9qY.L2', 'admin', 'System', 'Admin', '+91-9999999999', 1),
('john.doe@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdXdZSk9qY.L2', 'resident', 'John', 'Doe', '+91-9876543210', 1),
('worker1@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBdXdZSk9qY.L2', 'worker', 'Mike', 'Smith', '+91-9876543211', NULL);

-- Insert sample utility consumption data
INSERT INTO utility_consumption (building_id, utility_type, consumption_value, unit, recorded_date) VALUES
(1, 'water', 15000, 'liters', '2024-01-01'),
(1, 'electricity', 2500, 'kwh', '2024-01-01'),
(2, 'water', 25000, 'liters', '2024-01-01'),
(2, 'electricity', 4500, 'kwh', '2024-01-01');
