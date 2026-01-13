-- Run this in Supabase SQL Editor
-- 1. Resize password_hash column to hold longer scrypt hashes
ALTER TABLE users ALTER COLUMN password_hash TYPE VARCHAR(256);

-- 2. Update admin password to 'admin123' (valid scrypt format)
UPDATE users 
SET password_hash = 'scrypt:32768:8:1$zau1remTtC4hnHit$aebdae48923824619ffe93af9a4f05c5c81577abef48e030c26dda0fcfb8b10d55aa5fff0fa1a35cc62bab205c3a702655eb3a6a60b5f1ebcd5a06e360f9a1fa'
WHERE username = 'admin';

-- Verify
SELECT username, password_hash FROM users WHERE username = 'admin';
