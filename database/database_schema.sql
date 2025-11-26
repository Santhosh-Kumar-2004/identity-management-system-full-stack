CREATE DATABASE user_management_dev;

-- Using the DATABASE and Using it
USE user_management_dev; 

CREATE TABLE users(
	id VARCHAR(36) PRIMARY KEY NOT NULL, 
    name VARCHAR(255) NOT NULL, 
    email VARCHAR(255) UNIQUE NOT NULL, 
    password VARCHAR(255) NOT NULL, 
    role VARCHAR(20) NOT NULL DEFAULT 'user', 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

DROP TABLE users;

INSERT INTO users('id', 'name', 'email', 'password', 'role', 'created_at', 'updated_at')
VALUES ('550e8400-e29b-41d4-a716-446655440000', 'santhosh', 'santhosh@gmail.com', 'hvjvjh', 'admin');




