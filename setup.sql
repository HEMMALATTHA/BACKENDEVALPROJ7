-- 1. Create database
CREATE DATABASE payroll_db;

-- 2. Create a new user (replace 'password' with a strong password)
CREATE USER 'payroll_user'@'localhost' IDENTIFIED BY 'password';

-- 3. Grant all privileges to this user for your database
GRANT ALL PRIVILEGES ON payroll_db.* TO 'payroll_user'@'localhost';

-- 4. Apply changes
FLUSH PRIVILEGES;
