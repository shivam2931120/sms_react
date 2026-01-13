-- Run this in Supabase SQL Editor (Dashboard -> SQL Editor -> New Query)
-- This creates all tables and an admin user for SMS

-- 1. USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(20) DEFAULT 'student'
);

-- 2. DEPARTMENTS TABLE
CREATE TABLE IF NOT EXISTS departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20),
    head_teacher_id INTEGER
);

-- 3. CLASSES TABLE
CREATE TABLE IF NOT EXISTS classes (
    id SERIAL PRIMARY KEY,
    grade VARCHAR(20) NOT NULL,
    section VARCHAR(10) NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    class_teacher_id INTEGER
);

-- 4. TEACHERS TABLE
CREATE TABLE IF NOT EXISTS teachers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    qualification VARCHAR(100),
    specialization VARCHAR(100),
    phone VARCHAR(20),
    joining_date DATE
);

-- 5. STUDENTS TABLE
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    class_id INTEGER REFERENCES classes(id),
    department_id INTEGER REFERENCES departments(id),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    roll_no VARCHAR(20) UNIQUE,
    enrollment_no VARCHAR(30) UNIQUE,
    dob DATE,
    gender VARCHAR(10),
    blood_group VARCHAR(5),
    phone VARCHAR(20),
    parent_name VARCHAR(100),
    parent_phone VARCHAR(20),
    address TEXT,
    admission_date DATE,
    photo_file VARCHAR(100) DEFAULT 'default.jpg'
);

-- 6. SUBJECTS TABLE
CREATE TABLE IF NOT EXISTS subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20),
    department_id INTEGER REFERENCES departments(id)
);

-- 7. EXAMS TABLE
CREATE TABLE IF NOT EXISTS exams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    date DATE,
    subject_id INTEGER REFERENCES subjects(id)
);

-- 8. MARKS TABLE
CREATE TABLE IF NOT EXISTS marks (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) NOT NULL,
    subject_id INTEGER REFERENCES subjects(id) NOT NULL,
    exam_id INTEGER REFERENCES exams(id),
    score_obtained FLOAT,
    max_score FLOAT DEFAULT 100
);

-- 9. ATTENDANCE TABLE
CREATE TABLE IF NOT EXISTS attendance (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Absent'
);

-- 10. FEES TABLE
CREATE TABLE IF NOT EXISTS fees (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) NOT NULL,
    amount FLOAT NOT NULL,
    description VARCHAR(200),
    due_date DATE,
    paid_date DATE,
    status VARCHAR(20) DEFAULT 'Pending'
);

-- 11. TIMETABLE TABLE
CREATE TABLE IF NOT EXISTS time_table (
    id SERIAL PRIMARY KEY,
    class_id INTEGER REFERENCES classes(id),
    subject_id INTEGER REFERENCES subjects(id),
    teacher_id INTEGER REFERENCES teachers(id),
    day VARCHAR(20),
    start_time TIME,
    end_time TIME,
    room VARCHAR(50)
);

-- 12. ANNOUNCEMENTS TABLE
CREATE TABLE IF NOT EXISTS announcements (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    priority VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 13. HOMEWORK TABLE
CREATE TABLE IF NOT EXISTS homework (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    class_id INTEGER REFERENCES classes(id),
    subject_id INTEGER REFERENCES subjects(id),
    teacher_id INTEGER REFERENCES teachers(id),
    assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date DATE
);

-- 14. BOOKS TABLE
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100),
    isbn VARCHAR(20),
    copies INTEGER DEFAULT 1,
    available INTEGER DEFAULT 1
);

-- 15. BOOK ISSUES TABLE
CREATE TABLE IF NOT EXISTS book_issues (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books(id),
    student_id INTEGER REFERENCES students(id),
    issue_date DATE,
    return_date DATE,
    status VARCHAR(20) DEFAULT 'Issued'
);

-- 16. EVENTS TABLE
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    color VARCHAR(20) DEFAULT '#3788d8'
);

-- 17. ID CARDS TABLE
CREATE TABLE IF NOT EXISTS id_cards (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    card_number VARCHAR(50),
    issued_date DATE,
    expiry_date DATE
);

-- ============================================
-- CREATE ADMIN USER
-- Password: admin123 (bcrypt hash)
-- ============================================
INSERT INTO users (username, email, password_hash, role) 
VALUES (
    'admin', 
    'admin@sms.edu', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4EajKOXqWXBzFN4K',
    'admin'
) ON CONFLICT (username) DO NOTHING;

-- Create a sample department
INSERT INTO departments (name, code) 
VALUES ('Computer Science', 'CS')
ON CONFLICT DO NOTHING;

SELECT 'Setup complete! Login with admin / admin123' as message;
