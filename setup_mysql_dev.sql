-- Script prepares a MYSQL server for the project
-- First, create a database
-- Create a new user in localhost
-- Grant user all privileges on selected database
-- Grant user SELECT privilege on 'performance_schema' db
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
