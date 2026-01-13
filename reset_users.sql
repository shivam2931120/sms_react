-- WARNING: THIS WILL DELETE ALL USERS
DELETE FROM users;

-- Reset the ID sequence
ALTER SEQUENCE users_id_seq RESTART WITH 1;

-- Create the Custom Admin User
INSERT INTO users (username, email, password_hash, role) 
VALUES (
    'Shivam', 
    'shivam.bgp@outlook.com', 
    'scrypt:32768:8:1$oLN0YmKv7CYCYImG$6c21ebdcbf4c13e827f205d4137b86a1e38469e5cb800dc9376af7f581328779965e0ef69ce1a2df659f6cdd0d0b67519a3b13371ded11cacb0c1439acd70ae8', 
    'admin'
);

SELECT * FROM users;
