from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import Student, Teacher, User, Class, Subject
from sqlalchemy import or_

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/search')
@login_required
def search():
    query = request.args.get('q', '').strip()
    context = request.args.get('context', 'all').lower()
    
    if not query:
        return render_template('search_results.html', query=query, context=context,
                               students=[], teachers=[], users=[], classes=[], subjects=[])
    
    students = []
    teachers = []
    users = []
    classes = []
    subjects = []
    
    # Context-aware search
    if context == 'students' or context == 'all':
        students = Student.query.filter(
            or_(
                Student.first_name.ilike(f'%{query}%'),
                Student.last_name.ilike(f'%{query}%'),
                Student.roll_no.ilike(f'%{query}%'),
            )
        ).limit(20).all()
    
    if context == 'teachers' or context == 'all':
        teachers = Teacher.query.filter(
            or_(
                Teacher.first_name.ilike(f'%{query}%'),
                Teacher.last_name.ilike(f'%{query}%'),
            )
        ).limit(20).all()
    
    if context == 'users' or context == 'all':
        users = User.query.filter(
            or_(
                User.username.ilike(f'%{query}%'),
                User.email.ilike(f'%{query}%')
            )
        ).limit(20).all()
    
    if context == 'classes' or context == 'all':
        classes = Class.query.filter(
            or_(
                Class.grade.ilike(f'%{query}%'),
                Class.section.ilike(f'%{query}%'),
            )
        ).limit(20).all()
    
    if context == 'subjects' or context == 'all':
        subjects = Subject.query.filter(
            or_(
                Subject.name.ilike(f'%{query}%'),
                Subject.code.ilike(f'%{query}%'),
            )
        ).limit(20).all()

    return render_template('search_results.html', 
                           query=query,
                           context=context,
                           students=students, 
                           teachers=teachers, 
                           users=users,
                           classes=classes,
                           subjects=subjects)
