CREATE DATABASE IF NOT EXISTS smart_agriculture CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE smart_agriculture;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    location VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    rating TINYINT NOT NULL,
    comments TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE
    SET NULL
);
CREATE TABLE vendors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category ENUM('Seed', 'Fertilizer', 'Pesticide', 'Farmer Shop') NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone VARCHAR(30),
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE crop_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    crop VARCHAR(100) NOT NULL,
    area DECIMAL(10, 2) NOT NULL,
    rainfall DECIMAL(10, 2) NOT NULL,
    temperature DECIMAL(6, 2) NOT NULL,
    soil_type VARCHAR(80) NOT NULL,
    predicted_yield DECIMAL(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE disease_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    image_path VARCHAR(255),
    disease_name VARCHAR(150) NOT NULL,
    confidence DECIMAL(5, 2) NOT NULL,
    treatment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE weather_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    temperature DECIMAL(6, 2),
    humidity DECIMAL(6, 2),
    payload JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE
    SET NULL
);
CREATE TABLE chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
INSERT INTO vendors(
        name,
        category,
        address,
        phone,
        latitude,
        longitude
    )
VALUES (
        'Green Valley Seeds',
        'Seed',
        'Market Road, Bengaluru',
        '+91 98765 10001',
        12.9716,
        77.5946
    ),
(
        'Farm Care Fertilizers',
        'Fertilizer',
        'MG Road, Bengaluru',
        '+91 98765 10002',
        12.9750,
        77.6060
    ),
(
        'Crop Shield Store',
        'Pesticide',
        'Indiranagar, Bengaluru',
        '+91 98765 10003',
        12.9784,
        77.6408
    ),
(
        'Farmer Supply Hub',
        'Farmer Shop',
        'Jayanagar, Bengaluru',
        '+91 98765 10004',
        12.9250,
        77.5938
    );