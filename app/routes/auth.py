from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Student, Teacher
from app import db
from sqlalchemy import or_, text
import secrets
from datetime import datetime, timedelta

auth = Blueprint('auth', __name__)

# Store password reset tokens (in production, use database or Redis)
reset_tokens = {}

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
            db.session.execute(text('SELECT 1'))
            
            user = User.query.filter(
                or_(User.email == login_input, User.username == login_input)
            ).first()
            
            if user:
                if user.check_password(password):
                    login_user(user)
                    flash('Login successful!', 'success')
                    
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
                error_message = f'User "{login_input}" not found.'
                
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

# ============================================
# PASSWORD RESET
# ============================================
@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        user = User.query.filter(
            or_(User.email == email, User.username == email)
        ).first()
        
        if user:
            # Generate reset token
            token = secrets.token_urlsafe(32)
            reset_tokens[token] = {
                'user_id': user.id,
                'expires': datetime.now() + timedelta(hours=1)
            }
            
            # In production, send email. For now, show the link
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            flash(f'Password reset link (valid 1 hour): {reset_url}', 'info')
            print(f"\n🔑 PASSWORD RESET LINK: {reset_url}\n")
        else:
            flash('If that account exists, a reset link has been sent.', 'info')
        
        return redirect(url_for('auth.forgot_password'))
    
    return render_template('auth/forgot_password.html')

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Validate token
    if token not in reset_tokens:
        flash('Invalid or expired reset link.', 'danger')
        return redirect(url_for('auth.login'))
    
    token_data = reset_tokens[token]
    if datetime.now() > token_data['expires']:
        del reset_tokens[token]
        flash('Reset link has expired.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'warning')
            return redirect(url_for('auth.reset_password', token=token))
        
        if password != confirm:
            flash('Passwords do not match.', 'warning')
            return redirect(url_for('auth.reset_password', token=token))
        
        user = User.query.get(token_data['user_id'])
        if user:
            user.set_password(password)
            db.session.commit()
            del reset_tokens[token]
            flash('Password reset successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', token=token)

# ============================================
# PROFILE MANAGEMENT
# ============================================
@auth.route('/profile')
@login_required
def profile():
    # Get role-specific profile
    profile_data = None
    if current_user.role == 'teacher':
        profile_data = Teacher.query.filter_by(user_id=current_user.id).first()
    elif current_user.role == 'student':
        profile_data = Student.query.filter_by(user_id=current_user.id).first()
    
    return render_template('auth/profile.html', profile=profile_data)

@auth.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    email = request.form.get('email', '').strip()
    
    # Check if email is taken by another user
    existing = User.query.filter(User.email == email, User.id != current_user.id).first()
    if existing:
        flash('Email already in use.', 'danger')
        return redirect(url_for('auth.profile'))
    
    # Update user
    current_user.email = email
    
    # Update role-specific profile
    if current_user.role == 'teacher':
        profile = Teacher.query.filter_by(user_id=current_user.id).first()
        if profile:
            profile.phone = request.form.get('phone', '')
    elif current_user.role == 'student':
        profile = Student.query.filter_by(user_id=current_user.id).first()
        if profile:
            profile.phone = request.form.get('phone', '')
    
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('auth.profile'))

@auth.route('/profile/password', methods=['POST'])
@login_required
def change_password():
    current_pwd = request.form.get('current_password', '')
    new_pwd = request.form.get('new_password', '')
    confirm_pwd = request.form.get('confirm_password', '')
    
    if not current_user.check_password(current_pwd):
        flash('Current password is incorrect.', 'danger')
        return redirect(url_for('auth.profile'))
    
    if len(new_pwd) < 6:
        flash('New password must be at least 6 characters.', 'warning')
        return redirect(url_for('auth.profile'))
    
    if new_pwd != confirm_pwd:
        flash('New passwords do not match.', 'warning')
        return redirect(url_for('auth.profile'))
    
    current_user.set_password(new_pwd)
    db.session.commit()
    flash('Password changed successfully!', 'success')
    return redirect(url_for('auth.profile'))
