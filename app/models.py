from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'teacher', 'student'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student_profile = db.relationship('Student', backref='user', uselist=False, lazy=True)
    teacher_profile = db.relationship('Teacher', backref='user', uselist=False, lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(20), nullable=False)  # e.g. "1st Year", "2nd Year"
    section = db.Column(db.String(10), nullable=False)  # e.g. "A", "B"
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    class_teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    
    # Relationships
    students = db.relationship('Student', backref='enrolled_class', lazy=True)
    time_table = db.relationship('TimeTable', backref='class_info', lazy=True)
    department = db.relationship('Department', backref='classes', foreign_keys=[department_id])
    class_teacher = db.relationship('Teacher', backref='class_incharge', foreign_keys=[class_teacher_id])

    def __repr__(self):
        return f'<Class {self.grade}-{self.section}>'

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    
    # Relationships
    marks = db.relationship('Mark', backref='subject', lazy=True)
    time_table = db.relationship('TimeTable', backref='subject', lazy=True)

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    qualification = db.Column(db.String(100))
    specialization = db.Column(db.String(100))  # Subject expertise
    phone = db.Column(db.String(20))
    joining_date = db.Column(db.Date)
    
    # Relationships
    department = db.relationship('Department', backref='teachers', foreign_keys=[department_id])
    classes_managed = db.relationship('TimeTable', backref='teacher', lazy=True)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    
    # Personal Info
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    roll_no = db.Column(db.String(20), unique=True)
    enrollment_no = db.Column(db.String(30), unique=True)  # College enrollment number
    dob = db.Column(db.Date)
    gender = db.Column(db.String(10))
    blood_group = db.Column(db.String(5))
    
    # Contact & Guardian
    phone = db.Column(db.String(20))
    parent_name = db.Column(db.String(100))
    parent_phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    
    # Academic
    admission_date = db.Column(db.Date)
    
    # Relationships
    department = db.relationship('Department', backref='students', foreign_keys=[department_id])
    photo_file = db.Column(db.String(100), default='default.jpg') # filename
    
    # Relationships
    attendance = db.relationship('Attendance', backref='student', lazy=True)
    marks = db.relationship('Mark', backref='student', lazy=True)
    fees = db.relationship('Fee', backref='student', lazy=True)

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False) # 'Present', 'Absent', 'Late'
    remarks = db.Column(db.String(255))

class Exam(db.Model):
    __tablename__ = 'exams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # e.g. "Midterm 2024"
    date = db.Column(db.Date)
    
    marks = db.relationship('Mark', backref='exam', lazy=True)

class Mark(db.Model):
    __tablename__ = 'marks'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    score_obtained = db.Column(db.Float, nullable=False)
    max_score = db.Column(db.Float, nullable=False)

class Fee(db.Model):
    __tablename__ = 'fees'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False) # e.g. "Term 1 Fee"
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='Pending') # 'Paid', 'Pending', 'Overdue'
    paid_date = db.Column(db.Date)

class TimeTable(db.Model):
    # Mapping Table: Class + Subject + Teacher + Time (Simple version)
    __tablename__ = 'timetable'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    day_of_week = db.Column(db.String(20)) # Monday, Tuesday...
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

# ============================================
# NEW FEATURES MODELS
# ============================================

class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='normal')  # 'low', 'normal', 'high', 'urgent'
    target_role = db.Column(db.String(20), default='all')  # 'all', 'students', 'teachers', 'admin'
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    author = db.relationship('User', backref='announcements')

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100))
    isbn = db.Column(db.String(20), unique=True)
    category = db.Column(db.String(50))  # 'textbook', 'reference', 'fiction', etc.
    total_copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    issues = db.relationship('BookIssue', backref='book', lazy=True)

class BookIssue(db.Model):
    __tablename__ = 'book_issues'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='issued')  # 'issued', 'returned', 'overdue'
    fine_amount = db.Column(db.Float, default=0.0)
    
    student = db.relationship('Student', backref='book_issues')

class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # e.g., 'manage_students', 'view_reports'
    description = db.Column(db.String(200))

class RolePermission(db.Model):
    __tablename__ = 'role_permissions'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'teacher', 'student'
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), nullable=False)
    
    permission = db.relationship('Permission', backref='role_permissions')

# ============================================
# DEPARTMENT SYSTEM
# ============================================
class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # e.g., 'Science', 'Commerce', 'Arts', 'Sports'
    code = db.Column(db.String(20), unique=True)
    description = db.Column(db.Text)
    head_teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    head_teacher = db.relationship('Teacher', backref='headed_department', foreign_keys=[head_teacher_id])
    subjects = db.relationship('Subject', backref='department', lazy=True)

# ============================================
# CALENDAR / EVENTS
# ============================================
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50))  # 'exam', 'holiday', 'meeting', 'sports', 'cultural', 'deadline'
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    all_day = db.Column(db.Boolean, default=True)
    color = db.Column(db.String(20), default='#E10600')  # For calendar display
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    target_role = db.Column(db.String(20), default='all')  # 'all', 'students', 'teachers'
    
    creator = db.relationship('User', backref='created_events')

# ============================================
# HOMEWORK TRACKER
# ============================================
class Homework(db.Model):
    __tablename__ = 'homework'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date, nullable=False)
    assigned_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    class_info = db.relationship('Class', backref='homework_list')
    subject = db.relationship('Subject', backref='homework_list')
    teacher = db.relationship('Teacher', backref='assigned_homework')

# ============================================
# STUDENT ID CARDS
# ============================================
class IDCard(db.Model):
    __tablename__ = 'id_cards'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    card_number = db.Column(db.String(50), unique=True)
    issue_date = db.Column(db.Date, default=datetime.utcnow)
    expiry_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    
    student = db.relationship('Student', backref='id_card')
