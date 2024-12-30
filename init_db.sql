-- -- Create Database
-- DROP DATABASE IF EXISTS Delivery;
-- CREATE DATABASE Delivery;
-- USE Delivery;

DROP TABLE IF EXISTS VerifyToken;
DROP TABLE IF EXISTS ResetToken;
DROP TABLE IF EXISTS Act;
DROP TABLE IF EXISTS Deliver;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Resource;
DROP TABLE IF EXISTS Station;
DROP TABLE IF EXISTS Role;
DROP TABLE IF EXISTS AddressInfo;
DROP TABLE IF EXISTS User;

-- Create User Table
CREATE TABLE IF NOT EXISTS User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT TRUE
);

-- Creat Role Table
CREATE TABLE IF NOT EXISTS Role (
    role_name VARCHAR(255) PRIMARY KEY,
    description TEXT NOT NULL
);

-- Create Act Table
CREATE TABLE IF NOT EXISTS Act (
    user_id INT NOT NULL,
    role_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id, role_name),
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (role_name) REFERENCES Role(role_name)
);

-- Create AddressInfo Table
CREATE TABLE IF NOT EXISTS AddressInfo (
    address_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address_line_1 VARCHAR(255) NOT NULL,
    address_line_2 VARCHAR(255),
    zip_code VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- Create Station Table
CREATE TABLE IF NOT EXISTS Station (
    station_id INT AUTO_INCREMENT PRIMARY KEY,
    station_name VARCHAR(255) NOT NULL,
    address_line_1 VARCHAR(255) NOT NULL,
    address_line_2 VARCHAR(255),
    zip_code VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    max_drone_capacity INT NOT NULL,
    max_robot_capacity INT NOT NULL,
    current_drone_count INT NOT NULL,
    current_robot_count INT NOT NULL,
    current_available_drone_count INT NOT NULL,
    current_available_robot_count INT NOT NULL,
    current_working_drone_count INT NOT NULL,
    current_working_robot_count INT NOT NULL,
    dispatch_strategy VARCHAR(255) NOT NULL,
    enabled BOOLEAN NOT NULL
);

-- Create Order Table
CREATE TABLE IF NOT EXISTS Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,          
    user_id INT NOT NULL,                             
    station_id INT NOT NULL,
    delivery_src_address_id INT NOT NULL,            
    delivery_dst_address_id INT NOT NULL,            
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expected_at TIMESTAMP NOT NULL,   
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
    reserved_at TIMESTAMP DEFAULT NULL,              
    order_status ENUM('pending', 'in_progress', 'completed', 'canceled', 'failed') NOT NULL DEFAULT 'pending',
    total_price DECIMAL(10, 2) NOT NULL,
    delivery_method ENUM('robot', 'drone') NOT NULL,
    category VARCHAR(255) NOT NULL,
    payload DECIMAL(10, 2) NOT NULL,
    package_size VARCHAR(255) NOT NULL,
    note TEXT,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (delivery_src_address_id) REFERENCES AddressInfo(address_id), 
    FOREIGN KEY (delivery_dst_address_id) REFERENCES AddressInfo(address_id),
    FOREIGN KEY (station_id) REFERENCES Station(station_id)  
);

-- Create Resource Table
CREATE TABLE IF NOT EXISTS Resource (
    resource_id INT AUTO_INCREMENT PRIMARY KEY,
    station_id INT NOT NULL,
    type ENUM('robot', 'drone') NOT NULL,
    status ENUM('available', 'working', 'maintaining') NOT NULL DEFAULT 'available',
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    max_range DECIMAL(10, 2) NOT NULL,
    max_payload DECIMAL(10, 2) NOT NULL,
    speed DECIMAL(10, 2) NOT NULL,
    battery_level DECIMAL(10, 2) NOT NULL,
    enabled BOOLEAN NOT NULL,
    FOREIGN KEY (station_id) REFERENCES Station(station_id)
);

-- Create Deliver Table
CREATE TABLE IF NOT EXISTS Deliver (
    order_id INT NOT NULL,
    resource_id INT NOT NULL,
    PRIMARY KEY (order_id, resource_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (resource_id) REFERENCES Resource(resource_id)
);

-- Create ResetToken Table
CREATE TABLE IF NOT EXISTS ResetToken (
    token_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- Create VerifyToken Table
CREATE TABLE IF NOT EXISTS VerifyToken (
    token_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL
);

-- Insert Role Table
INSERT INTO Role (role_name, description) VALUES
('user', 'A regular client who receives services'),
('staff', 'An internal staff member');

-- Insert User Table
INSERT INTO User (username, password_hash, first_name, last_name, email, enabled) VALUES 
('admin', 'admin', 'admin', 'admin', 'admin@example.com', TRUE),
('yc7766', 'yc7766', 'yc7766', 'yc7766', 'yc7766@nyu.edu', TRUE);

-- Initalize Act Table
INSERT INTO Act (user_id, role_name) VALUES
(1, 'user'),
(1, 'staff'),
(2, 'user');