from app import create_app, db
from app.models import User, Student, Teacher, Department, Class
from datetime import date

app = create_app()

with app.app_context():
    # Ensure departments exist
    dept = Department.query.first()
    if not dept:
        dept = Department(name='General', code='GEN')
        db.session.add(dept)
        db.session.commit()

    # Ensure class exists
    cls = Class.query.first()
    if not cls:
        cls = Class(grade='10', section='A', department_id=dept.id)
        db.session.add(cls)
        db.session.commit()

    # Create Teacher
    teacher_user = User.query.filter_by(email='teacher@sms.com').first()
    if not teacher_user:
        teacher_user = User(username='teacher', email='teacher@sms.com', role='teacher')
        teacher_user.set_password('teacher123')
        db.session.add(teacher_user)
        db.session.flush()
        
        teacher = Teacher(
            user_id=teacher_user.id,
            first_name='John',
            last_name='Teacher',
            department_id=dept.id,
            phone='1234567890',
            joining_date=date.today()
        )
        db.session.add(teacher)
        db.session.commit()
        print("Teacher user created: teacher / teacher123")
    else:
        print("Teacher user already exists")

    # Create Student
    student_user = User.query.filter_by(email='student@sms.com').first()
    if not student_user:
        student_user = User(username='student', email='student@sms.com', role='student')
        student_user.set_password('student123')
        db.session.add(student_user)
        db.session.flush()
        
        student = Student(
            user_id=student_user.id,
            first_name='Jane',
            last_name='Student',
            roll_no='101',
            class_id=cls.id,
            department_id=dept.id,
            gender='Female',
            admission_date=date.today()
        )
        db.session.add(student)
        db.session.commit()
        print("Student user created: student / student123")
    else:
        print("Student user already exists")
