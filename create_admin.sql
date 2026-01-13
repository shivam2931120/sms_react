-- Run this in Supabase SQL Editor to add the admin user
-- Go to: Dashboard -> SQL Editor -> New Query -> Paste this -> Run

-- First check if users table exists, if not create it
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(20) DEFAULT 'student'
);

-- Delete existing admin if any (to reset password)
DELETE FROM users WHERE username = 'admin';

-- Insert admin user with password: admin123
-- This is a valid bcrypt hash for 'admin123'
INSERT INTO users (username, email, password_hash, role) 
VALUES (
    'admin', 
    'admin@sms.edu', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4EajKOXqWXBzFN4K',
    'admin'
);

-- Verify the user was created
SELECT id, username, email, role FROM users WHERE username = 'admin';
