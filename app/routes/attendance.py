from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Attendance, Student, Class
from app import db
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')

@attendance_bp.route('/mark', methods=['GET', 'POST'])
@login_required
def mark_attendance():
    if current_user.role != 'teacher':
        flash('Access denied', 'danger')
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        class_id = request.form.get('class_id')
        date = request.form.get('date')
        students = Student.query.filter_by(class_id=class_id).all()
        
        for student in students:
            status = request.form.get(f'status_{student.id}')
            if status:
                att = Attendance(student_id=student.id, date=datetime.strptime(date, '%Y-%m-%d'), status=status)
                db.session.add(att)
        
        db.session.commit()
        flash('Attendance marked successfully', 'success')
        return redirect(url_for('teacher.dashboard'))
        
    classes = [] # In real app, fetch classes assigned to teacher
    return render_template('attendance/mark.html', classes=classes)
