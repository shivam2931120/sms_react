from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from datetime import date, timedelta
from app import db
from app.models import Student, Attendance, Fee, Mark, TimeTable, Homework, Event, Announcement

student = Blueprint('student', __name__, url_prefix='/student')

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'student':
            flash('Access denied.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@student.route('/dashboard')
@login_required
@student_required
def dashboard():
    student = Student.query.filter_by(user_id=current_user.id).first()
    if not student:
        flash('Student profile not found.', 'warning')
        return redirect(url_for('main.index'))
    
    # Attendance stats
    today = date.today()
    month_ago = today - timedelta(days=30)
    total_att = Attendance.query.filter(Attendance.student_id == student.id, Attendance.date >= month_ago).count()
    present_att = Attendance.query.filter(Attendance.student_id == student.id, Attendance.date >= month_ago, Attendance.status == 'Present').count()
    att_percentage = round((present_att / total_att * 100), 1) if total_att > 0 else 0
    
    # Fee status
    pending_fees = Fee.query.filter_by(student_id=student.id, status='Pending').count()
    
    # Recent marks
    recent_marks = Mark.query.filter_by(student_id=student.id).order_by(Mark.id.desc()).limit(5).all()
    
    # Upcoming homework
    upcoming_hw = Homework.query.filter(Homework.class_id == student.class_id, Homework.due_date >= today).order_by(Homework.due_date).limit(5).all()
    
    # Announcements
    announcements = Announcement.query.filter_by(is_active=True).order_by(Announcement.created_at.desc()).limit(3).all()
    
    return render_template('student/dashboard.html', 
                           student=student,
                           att_percentage=att_percentage,
                           pending_fees=pending_fees,
                           recent_marks=recent_marks,
                           upcoming_hw=upcoming_hw,
                           announcements=announcements)

@student.route('/attendance')
@login_required
@student_required
def attendance():
    student = Student.query.filter_by(user_id=current_user.id).first()
    attendance = Attendance.query.filter_by(student_id=student.id).order_by(Attendance.date.desc()).limit(60).all()
    
    # Calculate stats
    total = len(attendance)
    present = sum(1 for a in attendance if a.status == 'Present')
    absent = sum(1 for a in attendance if a.status == 'Absent')
    late = sum(1 for a in attendance if a.status == 'Late')
    
    return render_template('student/attendance.html', 
                           student=student,
                           attendance=attendance,
                           stats={'total': total, 'present': present, 'absent': absent, 'late': late})

@student.route('/marks')
@login_required
@student_required
def marks():
    student = Student.query.filter_by(user_id=current_user.id).first()
    marks = Mark.query.filter_by(student_id=student.id).order_by(Mark.id.desc()).all()
    
    # Group by exam
    exams = {}
    for m in marks:
        if m.exam_id not in exams:
            exams[m.exam_id] = {'exam': m.exam, 'marks': []}
        exams[m.exam_id]['marks'].append(m)
    
    return render_template('student/marks.html', student=student, exams=exams)

@student.route('/fees')
@login_required
@student_required
def fees():
    student = Student.query.filter_by(user_id=current_user.id).first()
    fees = Fee.query.filter_by(student_id=student.id).order_by(Fee.due_date.desc()).all()
    
    total_due = sum(f.amount for f in fees if f.status == 'Pending')
    total_paid = sum(f.amount for f in fees if f.status == 'Paid')
    
    return render_template('student/fees.html', student=student, fees=fees, total_due=total_due, total_paid=total_paid)

@student.route('/timetable')
@login_required
@student_required
def timetable():
    student = Student.query.filter_by(user_id=current_user.id).first()
    timetable = TimeTable.query.filter_by(class_id=student.class_id).order_by(TimeTable.day, TimeTable.start_time).all()
    
    # Group by day
    days = {}
    for t in timetable:
        if t.day not in days:
            days[t.day] = []
        days[t.day].append(t)
    
    return render_template('student/timetable.html', student=student, days=days)

@student.route('/homework')
@login_required
@student_required
def homework():
    student = Student.query.filter_by(user_id=current_user.id).first()
    homework = Homework.query.filter_by(class_id=student.class_id).order_by(Homework.due_date.desc()).limit(20).all()
    return render_template('student/homework.html', student=student, homework=homework)
