from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models import User, School, Grade, Subject, Term, SchoolClass

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    schools_count = School.query.count()
    users_count = User.query.filter_by(role='school').count()
    terms = Term.query.order_by(Term.year.desc(), Term.term_number.desc()).all()
    return render_template('admin/dashboard.html', 
                           schools_count=schools_count, 
                           users_count=users_count,
                           terms=terms)

@admin_bp.route('/schools')
@login_required
@admin_required
def schools():
    schools = School.query.order_by(School.name).all()
    return render_template('admin/schools.html', schools=schools)

@admin_bp.route('/schools/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_school():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        name_sinhala = request.form.get('name_sinhala', '').strip()
        division = request.form.get('division', '').strip()
        principal = request.form.get('principal_name', '').strip()
        phone = request.form.get('contact_phone', '').strip()
        email = request.form.get('contact_email', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not name or not username or not password:
            flash('Name, username and password are required.', 'danger')
            return redirect(url_for('admin.add_school'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('admin.add_school'))
        
        school = School(
            name=name,
            name_sinhala=name_sinhala or name,
            division=division,
            principal_name=principal,
            contact_phone=phone,
            contact_email=email
        )
        db.session.add(school)
        db.session.flush()
        
        user = User(
            username=username,
            email=email or f'{username}@school.local',
            role='school',
            school_id=school.id
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash(f'School "{name}" and user "{username}" created successfully.', 'success')
        return redirect(url_for('admin.schools'))
    
    return render_template('admin/add_school.html')

@admin_bp.route('/schools/<int:school_id>/toggle')
@login_required
@admin_required
def toggle_school(school_id):
    school = School.query.get_or_404(school_id)
    school.is_active = not school.is_active
    db.session.commit()
    flash(f'School status updated.', 'success')
    return redirect(url_for('admin.schools'))

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.order_by(User.role, User.username).all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/terms')
@login_required
@admin_required
def terms():
    terms = Term.query.order_by(Term.year.desc(), Term.term_number.desc()).all()
    return render_template('admin/terms.html', terms=terms)

@admin_bp.route('/terms/add', methods=['POST'])
@login_required
@admin_required
def add_term():
    year = request.form.get('year', type=int)
    term_number = request.form.get('term_number', type=int)
    name = request.form.get('name', '').strip()
    if year and term_number:
        if not Term.query.filter_by(year=year, term_number=term_number).first():
            t = Term(year=year, term_number=term_number, name=name or f'Term {term_number} - {year}')
            db.session.add(t)
            db.session.commit()
            flash('Term added.', 'success')
        else:
            flash('Term already exists.', 'warning')
    return redirect(url_for('admin.terms'))

@admin_bp.route('/subjects')
@login_required
@admin_required
def subjects():
    subjects = Subject.query.filter_by(school_id=None).order_by(Subject.code).all()
    return render_template('admin/subjects.html', subjects=subjects)

@admin_bp.route('/zone')
@login_required
@admin_required
def zone_overview():
    """Overall zonal results dashboard"""
    from app.models import Student, Mark, Term
    from sqlalchemy import func
    
    term = Term.query.filter_by(is_active=True).first()
    schools = School.query.filter_by(is_active=True).order_by(School.name).all()
    
    school_stats = []
    total_students = 0
    total_with_marks = 0
    
    for school in schools:
        students = Student.query.filter_by(school_id=school.id, is_active=True).count()
        total_students += students
        
        # Count students who have at least one mark in current term
        if term:
            marked = db.session.query(func.count(func.distinct(Mark.student_id))).join(Student).filter(
                Student.school_id == school.id,
                Mark.term_id == term.id
            ).scalar() or 0
        else:
            marked = 0
        total_with_marks += marked
        
        # Average of averages (rough)
        avg_score = None
        if term and marked > 0:
            avg_score = db.session.query(func.avg(Mark.score)).join(Student).filter(
                Student.school_id == school.id,
                Mark.term_id == term.id,
                Mark.is_absent == False,
                Mark.score != None
            ).scalar()
            if avg_score:
                avg_score = round(avg_score, 1)
        
        school_stats.append({
            'school': school,
            'students': students,
            'marked': marked,
            'avg': avg_score,
            'progress': round((marked / students * 100) if students else 0, 1)
        })
    
    # Sort by average descending for ranking
    ranked = sorted([s for s in school_stats if s['avg'] is not None], key=lambda x: x['avg'], reverse=True)
    
    return render_template('admin/zone_overview.html',
                           term=term,
                           schools=schools,
                           school_stats=school_stats,
                           ranked=ranked,
                           total_students=total_students,
                           total_with_marks=total_with_marks,
                           schools_count=len(schools))

@admin_bp.route('/zone/school/<int:school_id>')
@login_required
@admin_required
def zone_school_detail(school_id):
    """Admin view of a specific school's data"""
    from app.models import Student, Mark, Term, SchoolClass
    school = School.query.get_or_404(school_id)
    term = Term.query.filter_by(is_active=True).first()
    classes = SchoolClass.query.filter_by(school_id=school.id).all()
    students_count = Student.query.filter_by(school_id=school.id, is_active=True).count()
    
    return render_template('admin/zone_school.html',
                           school=school, term=term, classes=classes,
                           students_count=students_count)
