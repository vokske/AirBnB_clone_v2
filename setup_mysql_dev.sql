-- Script prepares a MYSQL server for the project

-- First, create a database
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create a new user in localhost
CREATE USER IF NOT EXISTS hbnb_dev@localhost IDENTIFIED BY 'hbnb_dev_db';

--Grant user all privileges on selected database
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Grant user SELECT privilege on 'performance_schema' db
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
