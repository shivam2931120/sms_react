from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'teacher':
            return redirect(url_for('teacher.dashboard'))
        elif current_user.role == 'student':
            return redirect(url_for('student.dashboard'))
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        login_id = request.form.get('login_id')
        password = request.form.get('password')
        
        print(f"DEBUG: Login attempt for '{login_id}'") # Debug log
        
        # specific for postgresql (ilike), but generic sqlalchemy 'ilike' usually works
        user = User.query.filter((User.email.ilike(login_id)) | (User.username.ilike(login_id))).first()
        
        if user:
             print(f"DEBUG: User found: {user.username}, Role: {user.role}")
             if user.check_password(password):
                 if not user.is_approved:
                     print("DEBUG: Account not approved.")
                     flash('Account pending approval. Please wait for an administrator to verify your details.', 'warning')
                     return render_template('auth/login.html')

                 print("DEBUG: Password correct. Logging in...")
                 login_user(user)
                 print(f"DEBUG: User {user.username} logged in. Current User: {current_user}")
                 flash('Login successful!', 'success')
                 
                 # Redirect based on role
                 if user.role == 'admin':
                     return redirect(url_for('admin.dashboard'))
                 elif user.role == 'teacher':
                     return redirect(url_for('teacher.dashboard'))
                 elif user.role == 'student':
                     return redirect(url_for('student.dashboard'))
                 
                 return redirect(url_for('main.index'))
             else:
                 print("DEBUG: Password INCORRECT.")
        else:
             print("DEBUG: User NOT found.")

        flash('Login Unsuccessful. Please check email and password', 'danger')
            
    return render_template('auth/login.html')

@auth.before_app_request
def check_approval_status():
    if current_user.is_authenticated and not current_user.is_approved:
        logout_user()
        flash('Your account is pending approval or has been suspended.', 'warning')
        return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('auth/register.html')
            
        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'danger')
            return render_template('auth/register.html')
            
        # Create User
        user = User(username=username, email=email, role=role, is_approved=False)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()
        
        # Create Placeholder Profile
        from app.models import Student, Teacher, Department, Class
        from datetime import date
        
        # Get default dependencies (Assuming 'GEN' dept exists from seed)
        dept = Department.query.filter_by(code='GEN').first()
        
        if role == 'student':
            student = Student(
                user_id=user.id,
                first_name=username, # Provisional
                last_name='(Pending)',
                department_id=dept.id if dept else None,
                admission_date=date.today()
            )
            db.session.add(student)
        elif role == 'teacher':
            teacher = Teacher(
                user_id=user.id,
                first_name=username, # Provisional
                last_name='(Pending)',
                department_id=dept.id if dept else None,
                joining_date=date.today()
            )
            db.session.add(teacher)
            
        db.session.commit()
        flash('Account created! Please wait for admin approval.', 'info')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
