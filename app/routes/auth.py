from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db
from sqlalchemy import or_, text

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

    error_message = None
    
    if request.method == 'POST':
        login_input = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        try:
            # Test database connection first
            db.session.execute(text('SELECT 1'))
            
            # Allow login with email OR username
            user = User.query.filter(
                or_(User.email == login_input, User.username == login_input)
            ).first()
            
            if user:
                if user.check_password(password):
                    login_user(user)
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
                    error_message = 'Wrong password. Please try again.'
            else:
                error_message = f'User "{login_input}" not found. Please check username/email.'
                
        except Exception as e:
            error_message = f'Database connection failed: {str(e)[:100]}'
            db.session.rollback()
    
    if error_message:
        flash(error_message, 'danger')
            
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Debug route to check database
@auth.route('/debug-db')
def debug_db():
    import os
    try:
        db.session.execute(text('SELECT 1'))
        result = db.session.execute(text('SELECT COUNT(*) FROM users')).scalar()
        db_url = os.environ.get('DATABASE_URL', 'Not set')
        # Hide password
        if db_url and '@' in db_url:
            parts = db_url.split('@')
            db_url = parts[0].split(':')[0] + ':***@' + parts[1]
        return f'DB Connected! Users count: {result}. URL: {db_url}'
    except Exception as e:
        return f'DB Error: {str(e)}'
