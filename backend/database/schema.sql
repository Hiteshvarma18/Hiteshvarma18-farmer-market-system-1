CREATE DATABASE farmer_db;

USE farmer_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    phone VARCHAR(10) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE crop_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,

    crop VARCHAR(100),

    market VARCHAR(100),

    price DECIMAL(10,2),

    date DATE
);

CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255)
);


INSERT INTO admins
(username,password)
VALUES
(
'admin',
'$2b$12$examplehashedpassword'
);

CREATE TABLE mandi_locations (
    id INT AUTO_INCREMENT PRIMARY KEY,

    mandi_name VARCHAR(100),

    district VARCHAR(100),

    latitude DECIMAL(10,6),

    longitude DECIMAL(10,6)
);

INSERT INTO mandi_locations
(mandi_name,district,latitude,longitude)
VALUES
('Vijayawada Mandi','Vijayawada',16.5062,80.6480),

('Guntur Mandi','Guntur',16.3067,80.4365),

('Eluru Mandi','Eluru',16.7107,81.0952);

CREATE TABLE update_logs (

id INT AUTO_INCREMENT PRIMARY KEY,

updated_at TIMESTAMP
DEFAULT CURRENT_TIMESTAMP,

rows_imported INT

);