from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import Student, Teacher, User
from sqlalchemy import or_

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/search')
@login_required
def search():
    query = request.args.get('q', '').strip()
    
    if not query:
        return render_template('search_results.html', query=query, students=[], teachers=[], users=[])
    
    # Search logic using ILIKE for case-insensitive matching
    # Students
    students = Student.query.filter(
        or_(
            Student.first_name.ilike(f'%{query}%'),
            Student.last_name.ilike(f'%{query}%'),
            Student.email.ilike(f'%{query}%'),
            Student.roll_no.ilike(f'%{query}%'),
            Student.enrollment_no.ilike(f'%{query}%') if hasattr(Student, 'enrollment_no') else False
        )
    ).limit(20).all()
    
    # Teachers
    teachers = Teacher.query.filter(
        or_(
            Teacher.first_name.ilike(f'%{query}%'),
            Teacher.last_name.ilike(f'%{query}%'),
            Teacher.specialization.ilike(f'%{query}%')
        )
    ).limit(20).all()
    
    # Users
    users = User.query.filter(
        or_(
            User.username.ilike(f'%{query}%'),
            User.email.ilike(f'%{query}%')
        )
    ).limit(20).all()

    return render_template('search_results.html', 
                           query=query, 
                           students=students, 
                           teachers=teachers, 
                           users=users)
