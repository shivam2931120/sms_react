-- DANGER: THIS WILL DELETE ALL EXISTING DATA
-- Run this in Supabase SQL Editor to Reset Database and Match Models exactly

-- Drop existing tables (Order matters due to foreign keys)
DROP TABLE IF EXISTS role_permissions CASCADE;
DROP TABLE IF EXISTS permissions CASCADE;
DROP TABLE IF EXISTS id_cards CASCADE;
DROP TABLE IF EXISTS homework CASCADE;
DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS book_issues CASCADE;
DROP TABLE IF EXISTS books CASCADE;
DROP TABLE IF EXISTS announcements CASCADE;
DROP TABLE IF EXISTS timetable CASCADE;
DROP TABLE IF EXISTS fees CASCADE;
DROP TABLE IF EXISTS marks CASCADE;
DROP TABLE IF EXISTS exams CASCADE;
DROP TABLE IF EXISTS subjects CASCADE;
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS teachers CASCADE;
DROP TABLE IF EXISTS classes CASCADE;
DROP TABLE IF EXISTS departments CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 1. USERS
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128),
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. DEPARTMENTS
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE,
    description TEXT,
    head_teacher_id INTEGER, -- FK added later to avoid circular dependency
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. TEACHERS
CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    department_id INTEGER REFERENCES departments(id),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    qualification VARCHAR(100),
    specialization VARCHAR(100),
    phone VARCHAR(20),
    joining_date DATE
);

-- Add circular FK for departments head_teacher
ALTER TABLE departments ADD CONSTRAINT fk_head_teacher FOREIGN KEY (head_teacher_id) REFERENCES teachers(id);

-- 4. CLASSES
CREATE TABLE classes (
    id SERIAL PRIMARY KEY,
    grade VARCHAR(20) NOT NULL,
    section VARCHAR(10) NOT NULL,
    department_id INTEGER REFERENCES departments(id),
    class_teacher_id INTEGER REFERENCES teachers(id)
);

-- 5. STUDENTS
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
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

-- 6. SUBJECTS
CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE,
    department_id INTEGER REFERENCES departments(id)
);

-- 7. EXAMS
CREATE TABLE exams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    date DATE
);

-- 8. MARKS
CREATE TABLE marks (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id),
    exam_id INTEGER NOT NULL REFERENCES exams(id),
    subject_id INTEGER NOT NULL REFERENCES subjects(id),
    score_obtained FLOAT NOT NULL,
    max_score FLOAT NOT NULL
);

-- 9. FEES
CREATE TABLE fees (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id),
    title VARCHAR(100) NOT NULL,
    amount FLOAT NOT NULL,
    due_date DATE,
    status VARCHAR(20) DEFAULT 'Pending',
    paid_date DATE
);

-- 10. TIMETABLE
CREATE TABLE timetable (
    id SERIAL PRIMARY KEY,
    class_id INTEGER NOT NULL REFERENCES classes(id),
    subject_id INTEGER NOT NULL REFERENCES subjects(id),
    teacher_id INTEGER NOT NULL REFERENCES teachers(id),
    day_of_week VARCHAR(20),
    start_time TIME WITHOUT TIME ZONE,
    end_time TIME WITHOUT TIME ZONE
);

-- 11. ANNOUNCEMENTS
CREATE TABLE announcements (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    priority VARCHAR(20) DEFAULT 'normal',
    target_role VARCHAR(20) DEFAULT 'all',
    created_by INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITHOUT TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE
);

-- 12. BOOKS
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100),
    isbn VARCHAR(20) UNIQUE,
    category VARCHAR(50),
    total_copies INTEGER DEFAULT 1,
    available_copies INTEGER DEFAULT 1,
    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 13. BOOK ISSUES
CREATE TABLE book_issues (
    id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books(id),
    student_id INTEGER NOT NULL REFERENCES students(id),
    issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP WITHOUT TIME ZONE,
    return_date TIMESTAMP WITHOUT TIME ZONE,
    status VARCHAR(20) DEFAULT 'issued',
    fine_amount FLOAT DEFAULT 0.0
);

-- 14. EVENTS
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    event_type VARCHAR(50),
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    all_day BOOLEAN DEFAULT TRUE,
    color VARCHAR(20) DEFAULT '#E10600',
    created_by INTEGER REFERENCES users(id),
    target_role VARCHAR(20) DEFAULT 'all'
);

-- 15. HOMEWORK
CREATE TABLE homework (
    id SERIAL PRIMARY KEY,
    class_id INTEGER NOT NULL REFERENCES classes(id),
    subject_id INTEGER NOT NULL REFERENCES subjects(id),
    teacher_id INTEGER NOT NULL REFERENCES teachers(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    due_date DATE NOT NULL,
    assigned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 16. ID CARDS
CREATE TABLE id_cards (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id),
    card_number VARCHAR(50) UNIQUE,
    issue_date DATE DEFAULT CURRENT_DATE,
    expiry_date DATE,
    is_active BOOLEAN DEFAULT TRUE
);

-- 17. PERMISSIONS
CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(200)
);

-- 18. ROLE PERMISSIONS
CREATE TABLE role_permissions (
    id SERIAL PRIMARY KEY,
    role VARCHAR(20) NOT NULL,
    permission_id INTEGER NOT NULL REFERENCES permissions(id)
);

-- ============================================
-- SEED DATA - ADMIN USER
-- ============================================
INSERT INTO users (username, email, password_hash, role) 
VALUES (
    'admin', 
    'admin@sms.edu', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4EajKOXqWXBzFN4K', -- admin123
    'admin'
);

SELECT 'Database Schema Reset Successfully' as status;
