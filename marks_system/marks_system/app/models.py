from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='school')  # 'admin' or 'school'
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    school = db.relationship('School', backref='users')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class School(db.Model):
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    name_sinhala = db.Column(db.String(200))
    division = db.Column(db.String(100))  # කොට්ඨාසය
    address = db.Column(db.Text)
    principal_name = db.Column(db.String(150))
    contact_phone = db.Column(db.String(20))
    contact_email = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    classes = db.relationship('SchoolClass', backref='school', lazy='dynamic')
    students = db.relationship('Student', backref='school', lazy='dynamic')
    subjects = db.relationship('Subject', backref='school', lazy='dynamic')

class Term(db.Model):
    __tablename__ = 'terms'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    term_number = db.Column(db.Integer, nullable=False)  # 1, 2, 3
    name = db.Column(db.String(100))  # e.g. "II වාර පරීක්ෂණය - 2026"
    is_active = db.Column(db.Boolean, default=True)
    
    __table_args__ = (db.UniqueConstraint('year', 'term_number', name='_year_term_uc'),)

class Grade(db.Model):
    """Grade levels 3-13"""
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)  # 3 to 13
    name = db.Column(db.String(50))  # "Grade 6"
    name_sinhala = db.Column(db.String(50))
    num_subjects_for_average = db.Column(db.Integer, default=0)  # from No of Subject sheet

class SchoolClass(db.Model):
    """e.g. 6-A, 10-B"""
    __tablename__ = 'school_classes'
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    grade_id = db.Column(db.Integer, db.ForeignKey('grades.id'), nullable=False)
    section = db.Column(db.String(5), nullable=False)  # A, B, C...
    class_teacher_name = db.Column(db.String(150))
    
    grade = db.relationship('Grade')
    students = db.relationship('Student', backref='school_class', lazy='dynamic')
    
    __table_args__ = (db.UniqueConstraint('school_id', 'grade_id', 'section', name='_school_grade_section_uc'),)
    
    @property
    def full_name(self):
        return f"{self.grade.number} - {self.section}"

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=True)  # null = global
    code = db.Column(db.String(20))  # e.g. subject number for O/L
    name = db.Column(db.String(100), nullable=False)
    name_sinhala = db.Column(db.String(100))
    category = db.Column(db.String(50))  # core, aesthetic, religion, basket, etc.
    is_aesthetic = db.Column(db.Boolean, default=False)  # for 6-9
    grade_from = db.Column(db.Integer, default=3)
    grade_to = db.Column(db.Integer, default=13)
    is_active = db.Column(db.Boolean, default=True)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('school_classes.id'), nullable=False)
    admission_no = db.Column(db.String(50))
    name = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(10))  # Male/Female or M/F or ස්ත්‍රී/පුරුෂ
    date_of_birth = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    marks = db.relationship('Mark', backref='student', lazy='dynamic', cascade='all, delete-orphan')

class Mark(db.Model):
    __tablename__ = 'marks'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    term_id = db.Column(db.Integer, db.ForeignKey('terms.id'), nullable=False)
    score = db.Column(db.Float)  # null or special for 'ab' absent
    is_absent = db.Column(db.Boolean, default=False)
    entered_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    subject = db.relationship('Subject')
    term = db.relationship('Term')
    
    __table_args__ = (db.UniqueConstraint('student_id', 'subject_id', 'term_id', name='_student_subject_term_uc'),)

class SystemSetting(db.Model):
    __tablename__ = 'system_settings'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    description = db.Column(db.String(255))
