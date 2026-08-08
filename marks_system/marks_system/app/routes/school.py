from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime
from app import db
from app.models import (School, SchoolClass, Student, Subject, Mark, Term, Grade, User)

school_bp = Blueprint('school', __name__)

def school_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'school':
            flash('School access required.', 'danger')
            return redirect(url_for('auth.login'))
        if not current_user.school or not current_user.school.is_active:
            flash('Your school account is inactive.', 'danger')
            return redirect(url_for('auth.logout'))
        return f(*args, **kwargs)
    return decorated

@school_bp.route('/')
@login_required
@school_required
def dashboard():
    school = current_user.school
    classes = SchoolClass.query.filter_by(school_id=school.id).all()
    students_count = Student.query.filter_by(school_id=school.id, is_active=True).count()
    active_term = Term.query.filter_by(is_active=True).first()
    return render_template('school/dashboard.html',
                           school=school,
                           classes=classes,
                           students_count=students_count,
                           active_term=active_term)

@school_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@school_required
def profile():
    school = current_user.school
    if request.method == 'POST':
        school.name = request.form.get('name', school.name).strip()
        school.name_sinhala = request.form.get('name_sinhala', school.name_sinhala).strip()
        school.division = request.form.get('division', school.division).strip()
        school.principal_name = request.form.get('principal_name', school.principal_name).strip()
        school.contact_phone = request.form.get('contact_phone', school.contact_phone).strip()
        school.contact_email = request.form.get('contact_email', school.contact_email).strip()
        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect(url_for('school.profile'))
    return render_template('school/profile.html', school=school)

@school_bp.route('/classes')
@login_required
@school_required
def classes():
    school = current_user.school
    classes = SchoolClass.query.filter_by(school_id=school.id).join(Grade).order_by(Grade.number, SchoolClass.section).all()
    grades = Grade.query.order_by(Grade.number).all()
    return render_template('school/classes.html', classes=classes, grades=grades)

@school_bp.route('/classes/add', methods=['POST'])
@login_required
@school_required
def add_class():
    school = current_user.school
    grade_id = request.form.get('grade_id', type=int)
    section = request.form.get('section', '').strip().upper()
    teacher = request.form.get('class_teacher_name', '').strip()
    
    if not grade_id or not section:
        flash('Grade and section required.', 'danger')
        return redirect(url_for('school.classes'))
    
    existing = SchoolClass.query.filter_by(school_id=school.id, grade_id=grade_id, section=section).first()
    if existing:
        flash('Class already exists.', 'warning')
        return redirect(url_for('school.classes'))
    
    cls = SchoolClass(
        school_id=school.id,
        grade_id=grade_id,
        section=section,
        class_teacher_name=teacher
    )
    db.session.add(cls)
    db.session.commit()
    flash(f'Class {cls.full_name} created.', 'success')
    return redirect(url_for('school.classes'))

@school_bp.route('/classes/<int:class_id>/students')
@login_required
@school_required
def class_students(class_id):
    school = current_user.school
    cls = SchoolClass.query.filter_by(id=class_id, school_id=school.id).first_or_404()
    students = Student.query.filter_by(class_id=cls.id, is_active=True).order_by(Student.name).all()
    return render_template('school/students.html', cls=cls, students=students)

@school_bp.route('/classes/<int:class_id>/students/add', methods=['POST'])
@login_required
@school_required
def add_student(class_id):
    school = current_user.school
    cls = SchoolClass.query.filter_by(id=class_id, school_id=school.id).first_or_404()
    
    name = request.form.get('name', '').strip()
    admission_no = request.form.get('admission_no', '').strip()
    gender = request.form.get('gender', '').strip()
    dob_str = request.form.get('date_of_birth', '').strip()
    
    if not name:
        flash('Student name is required.', 'danger')
        return redirect(url_for('school.class_students', class_id=class_id))
    
    dob = None
    if dob_str:
        try:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        except:
            pass
    
    student = Student(
        school_id=school.id,
        class_id=cls.id,
        name=name,
        admission_no=admission_no,
        gender=gender,
        date_of_birth=dob
    )
    db.session.add(student)
    db.session.commit()
    flash(f'Student {name} added.', 'success')
    return redirect(url_for('school.class_students', class_id=class_id))

@school_bp.route('/marks/<int:class_id>')
@login_required
@school_required
def marks_entry(class_id):
    school = current_user.school
    cls = SchoolClass.query.filter_by(id=class_id, school_id=school.id).first_or_404()
    term = Term.query.filter_by(is_active=True).first()
    if not term:
        flash('No active term. Contact admin.', 'warning')
        return redirect(url_for('school.dashboard'))
    
    students = Student.query.filter_by(class_id=cls.id, is_active=True).order_by(Student.name).all()
    
    # Subjects applicable for this grade
    subjects = Subject.query.filter(
        (Subject.school_id == None) | (Subject.school_id == school.id),
        Subject.grade_from <= cls.grade.number,
        Subject.grade_to >= cls.grade.number,
        Subject.is_active == True
    ).order_by(Subject.code).all()
    
    # Existing marks
    marks_map = {}
    for st in students:
        marks_map[st.id] = {}
        for m in Mark.query.filter_by(student_id=st.id, term_id=term.id).all():
            marks_map[st.id][m.subject_id] = m
    
    return render_template('school/marks_entry.html',
                           cls=cls, term=term, students=students,
                           subjects=subjects, marks_map=marks_map)

@school_bp.route('/marks/<int:class_id>/save', methods=['POST'])
@login_required
@school_required
def save_marks(class_id):
    school = current_user.school
    cls = SchoolClass.query.filter_by(id=class_id, school_id=school.id).first_or_404()
    term = Term.query.filter_by(is_active=True).first_or_404()
    
    data = request.get_json() or {}
    saved = 0
    
    for item in data.get('marks', []):
        student_id = item.get('student_id')
        subject_id = item.get('subject_id')
        value = item.get('value', '').strip()
        
        student = Student.query.filter_by(id=student_id, class_id=cls.id).first()
        if not student:
            continue
        
        is_absent = value.lower() in ('ab', 'abs', 'absent', '-')
        score = None
        if not is_absent and value:
            try:
                score = float(value)
                if score < 0 or score > 100:
                    continue
            except:
                continue
        
        mark = Mark.query.filter_by(student_id=student_id, subject_id=subject_id, term_id=term.id).first()
        if mark:
            mark.score = score
            mark.is_absent = is_absent
            mark.entered_by = current_user.id
        else:
            mark = Mark(
                student_id=student_id,
                subject_id=subject_id,
                term_id=term.id,
                score=score,
                is_absent=is_absent,
                entered_by=current_user.id
            )
            db.session.add(mark)
        saved += 1
    
    db.session.commit()
    return jsonify({'status': 'ok', 'saved': saved})

@school_bp.route('/reports/<int:class_id>')
@login_required
@school_required
def class_report(class_id):
    school = current_user.school
    cls = SchoolClass.query.filter_by(id=class_id, school_id=school.id).first_or_404()
    term = Term.query.filter_by(is_active=True).first()
    students = Student.query.filter_by(class_id=cls.id, is_active=True).order_by(Student.name).all()
    
    subjects = Subject.query.filter(
        (Subject.school_id == None) | (Subject.school_id == school.id),
        Subject.grade_from <= cls.grade.number,
        Subject.grade_to >= cls.grade.number,
        Subject.is_active == True
    ).order_by(Subject.code).all()
    
    # Compute totals, averages, ranks
    results = []
    for st in students:
        marks = {}
        total = 0
        count = 0
        for sub in subjects:
            m = Mark.query.filter_by(student_id=st.id, subject_id=sub.id, term_id=term.id).first()
            if m and not m.is_absent and m.score is not None:
                marks[sub.id] = m.score
                total += m.score
                count += 1
            elif m and m.is_absent:
                marks[sub.id] = 'ab'
            else:
                marks[sub.id] = None
        
        avg = round(total / count, 2) if count > 0 else 0
        results.append({
            'student': st,
            'marks': marks,
            'total': total,
            'average': avg,
            'count': count
        })
    
    # Rank by average
    results.sort(key=lambda x: x['average'], reverse=True)
    for i, r in enumerate(results):
        r['class_rank'] = i + 1
    
    return render_template('school/report.html',
                           school=school, cls=cls, term=term,
                           subjects=subjects, results=results)
