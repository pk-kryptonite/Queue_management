-- Database creation
CREATE DATABASE IF NOT EXISTS queue_management;

-- Use the created database
USE queue_management;

-- Table for storing organization information
CREATE TABLE IF NOT EXISTS organisation (
    org_id INT AUTO_INCREMENT PRIMARY KEY,
    org_name VARCHAR(100) NOT NULL,
    org_address VARCHAR(255),
    org_contact VARCHAR(20)
);

-- Table for storing admin information
CREATE TABLE IF NOT EXISTS admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,  -- Use appropriate hashing for real-world scenarios
    profile_picture VARCHAR(255),     -- Path to profile picture
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    org_id INT,
    FOREIGN KEY (org_id) REFERENCES organisation(org_id)
);

-- Table for storing services offered by organisation
CREATE TABLE IF NOT EXISTS services (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(50) NOT NULL,
    description TEXT, 
    start_time TIMESTAMP,
    endtime TIMESTAMP,
    org_id INT,
    FOREIGN KEY (org_id) REFERENCES organisation(org_id)
);

-- Table for storing customer information
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL, 
    time_passed TIME,
    queue_number INT NOT NULL
);

-- Table for storing queue information
CREATE TABLE IF NOT EXISTS queues (
    queue_id INT AUTO_INCREMENT PRIMARY KEY,
    queue_number INT NOT NULL,
    customer_id INT,
    admin_id INT,
    service_id INT,
    status ENUM('Queuing', 'Served') NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (service_id) REFERENCES services(service_id)
);

-- Insert organizations
INSERT INTO organisation (org_name, org_address, org_contact) VALUES
('Organization 1', 'Address 1', 'Contact 1'),
('Organization 2', 'Address 2', 'Contact 2');

-- Insert admins
INSERT INTO admins (username, password, profile_picture, org_id) VALUES
('admin1', 'hashed_password_1', '/path/to/profile1.jpg', 1),
('admin2', 'hashed_password_2', '/path/to/profile2.jpg', 2);

-- Insert services
INSERT INTO services (service_name, org_id) VALUES
('Service A', 1),
('Service B', 1),
('Service C', 2);
('Service D', 2);
('Service E', 2);

-- Insert customers
INSERT INTO customers (name, time_passed, queue_number) VALUES
('Customer 1', '03:00:00', 33),
('Customer 2', '01:00:00', 34),
('Customer 3', '01:00:00', 35);

-- Insert queues
INSERT INTO queues (queue_number, customer_id, service_id, status) VALUES
(33, 1, 1, 'Queuing'),
(34, 2, 2, 'Queuing'),
(35, 3, 3, 'Queuing');

