-- Script sets up a test db for the project on MYSQL server

-- Create a database
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create a new user
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on specific db
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grant SELECT privilege on 'performance_schema' db
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
