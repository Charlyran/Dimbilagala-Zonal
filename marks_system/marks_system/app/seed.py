from app import db
from app.models import User, Grade, Subject, Term, School

# 39 schools of Polonnaruwa Zone (PL)
ZONE_SCHOOLS = [
    "PL/WILAYAYA MADHYA MAHA VIDYALAYA",
    "PL/SIRIPURA MADHYA MAHA VIDYALAYA",
    "PL/WELIKANDA MAHA VIDYALAYA",
    "PL/WEHERAGALA MAHA VIDYALAYA",
    "PL/MEDAGAMA MAHA VIDYALAYA",
    "PL/SEVANAPITIYA MAHA VIDYALAYA",
    "PL/NIKAWATHALANDA MAHA VIDYALAYA",
    "PL/BOGASWEWA MAHA VIDYALAYA",
    "PL/LEELARATHNA WIJESINGHA MAHA VIDYALAYA",
    "PL/ELLEWEWA MAHA VIDYALAYA",
    "PL/ASELAPURA MAHA VIDYALAYA",
    "PL/NUWARAGALA MAHA VIDYALAYA",
    "PL/ALAWAKUMBURA MAHA VIDYALAYA",
    "PL/NELUMWEWA MAHA VIDYALAYA",
    "PL/MADURU OYA MAHA VIDYALAYA",
    "PL/MANAMPITIYA SINHALA MAHA VIDYALAYA",
    "PL/KASHYAPA MAHA VIDYALAYA",
    "PL/VIJAYA PARAKKRAMA KANISHTA VIDYALAYA",
    "PL/DAMMINNA MAHA VIDYALAYA",
    "PL/SINHAPURA KANISTA VIDYALAYA",
    "PL/PIHITIWEWA MAHA VIDYALAYA",
    "PL/KALINGAWILA KANISHTA VIDYALAYA",
    "PL/KADAWATHAMADUWA DHARMAPALA KANISHTA VIDYALAYA",
    "PL/BANDANAGALA KANISHTA VIDYALAYA",
    "PL/KANDEGAMA KANISHTA VIDYALAYA",
    "PL/PAHALA YAKKURE KANISHTA VIDYALAYA",
    "PL/PELATIYAWEWA SECONDARY SCHOOL",
    "PL/KEKULUWELA MAHA VIDYALAYA",
    "PL/NAWAPALLEGAMA VIDYALAYA",
    "PL/NAWAGINIDAMANA MAHA VIDYALAYA",
    "PL/IHALA YAKKURE KANISHTA VIDYALAYA",
    "PL/MAGULDAMANA MAHA VIDYALAYA",
    "PL/KATUWANWILA MUSLIM KANISHTA VIDYALAYA",
    "PL/SENAPURA AL AMEEN MUSLIM MAHA VIDYALAYA",
    "PL/MANAMPITIYA TAMIL MAHA VIDYALAYA",
    "PL/HEWANPITIYA TAMIL MAHA VIDYALAYA",
    "PL/MUTUGALA TAMIL VIDYALAYA",
    "PL/THRIKONAMADUWA MUSLIM MAHA VIDYALAYA",
    "PL/ROTAWEWA TAMIL KANISHTA VIDYALAYA",
]

def make_username(school_name):
    name = school_name.replace("PL/", "").strip()
    parts = name.split()
    key = parts[0].lower()
    if len(parts) > 1 and parts[1] not in ("MAHA", "MADHYA", "KANISHTA", "KANISTA", "SECONDARY", "SINHALA", "TAMIL", "MUSLIM", "AL"):
        key = (parts[0] + parts[1]).lower()
    elif len(parts) > 1:
        key = (parts[0] + parts[1][:4]).lower()
    key = ''.join(c for c in key if c.isalnum())
    return key[:18]

def seed_data():
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@zone.edu.lk', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        print("Admin user created: admin / admin123")
    
    for num in range(3, 14):
        if not Grade.query.filter_by(number=num).first():
            g = Grade(
                number=num,
                name=f'Grade {num}',
                name_sinhala=f'{num} ශ්‍රේණිය',
                num_subjects_for_average={3:6,4:6,5:6,6:12,7:12,8:12,9:12,10:9,11:9,12:4,13:4}.get(num, 6)
            )
            db.session.add(g)
    
    default_subjects = [
        {'code': '1', 'name': 'Mother Tongue', 'name_sinhala': 'මව් බස', 'category': 'core', 'grade_from': 3, 'grade_to': 13},
        {'code': '2', 'name': 'Religion', 'name_sinhala': 'ආගම', 'category': 'religion', 'grade_from': 3, 'grade_to': 13},
        {'code': '3', 'name': 'English', 'name_sinhala': 'ඉංග්‍රිසි', 'category': 'core', 'grade_from': 3, 'grade_to': 13},
        {'code': '4', 'name': 'Mathematics', 'name_sinhala': 'ගණිතය', 'category': 'core', 'grade_from': 3, 'grade_to': 13},
        {'code': '5', 'name': 'Science', 'name_sinhala': 'විද්‍යාව', 'category': 'core', 'grade_from': 6, 'grade_to': 11},
        {'code': '6', 'name': 'History', 'name_sinhala': 'ඉතිහාසය', 'category': 'core', 'grade_from': 6, 'grade_to': 11},
        {'code': '7', 'name': 'Geography', 'name_sinhala': 'භූගෝල විද්‍යාව', 'category': 'core', 'grade_from': 6, 'grade_to': 11},
        {'code': '8', 'name': 'Civic Education', 'name_sinhala': 'පුරවැසි අධ්‍යාපනය', 'category': 'core', 'grade_from': 6, 'grade_to': 11},
        {'code': '9', 'name': 'Second Language', 'name_sinhala': 'දෙවන බස', 'category': 'core', 'grade_from': 6, 'grade_to': 11},
        {'code': '10', 'name': 'Health & Physical Education', 'name_sinhala': 'සෞඛ්‍ය හා ශාරීරික අධ්‍යාපනය', 'category': 'core', 'grade_from': 6, 'grade_to': 11},
        {'code': '11', 'name': 'Practical & Technical Skills', 'name_sinhala': 'ප්‍රායෝගික හා තාක්ෂණික කුසලතා', 'category': 'core', 'grade_from': 6, 'grade_to': 9},
        {'code': '12', 'name': 'Music (Western)', 'name_sinhala': 'සංගීත(පෙ)', 'category': 'aesthetic', 'is_aesthetic': True, 'grade_from': 6, 'grade_to': 11},
        {'code': '13', 'name': 'Art', 'name_sinhala': 'චිත්‍ර', 'category': 'aesthetic', 'is_aesthetic': True, 'grade_from': 6, 'grade_to': 11},
        {'code': '14', 'name': 'Dancing (Traditional)', 'name_sinhala': 'නැටුම්(දේශිය)', 'category': 'aesthetic', 'is_aesthetic': True, 'grade_from': 6, 'grade_to': 11},
        {'code': '15', 'name': 'Drama & Theatre', 'name_sinhala': 'රංග කලාව', 'category': 'aesthetic', 'is_aesthetic': True, 'grade_from': 6, 'grade_to': 11},
        {'code': '16', 'name': 'ICT', 'name_sinhala': 'ICT', 'category': 'core', 'grade_from': 6, 'grade_to': 11},
        {'code': '31', 'name': 'Buddhism', 'name_sinhala': 'බුද්ධ ධර්මය', 'category': 'religion', 'grade_from': 10, 'grade_to': 11},
        {'code': '32', 'name': 'Catholicism', 'name_sinhala': 'කතෝලික', 'category': 'religion', 'grade_from': 10, 'grade_to': 11},
        {'code': '60', 'name': 'Business & Accounting', 'name_sinhala': 'ව්‍යාපාර හා ගිණුම්කරණය', 'category': 'basket', 'grade_from': 10, 'grade_to': 11},
    ]
    
    for s in default_subjects:
        if not Subject.query.filter_by(code=s['code'], school_id=None).first():
            sub = Subject(
                school_id=None, code=s['code'], name=s['name'], name_sinhala=s['name_sinhala'],
                category=s.get('category', 'core'), is_aesthetic=s.get('is_aesthetic', False),
                grade_from=s.get('grade_from', 3), grade_to=s.get('grade_to', 13)
            )
            db.session.add(sub)
    
    if not Term.query.filter_by(year=2026, term_number=2).first():
        t = Term(year=2026, term_number=2, name='II වාර පරීක්ෂණය - 2026', is_active=True)
        db.session.add(t)
    
    created_count = 0
    for full_name in ZONE_SCHOOLS:
        if School.query.filter_by(name=full_name).first():
            continue
        
        short = full_name.replace("PL/", "").strip()
        username = make_username(full_name)
        base_username = username
        counter = 1
        while User.query.filter_by(username=username).first():
            username = f"{base_username}{counter}"
            counter += 1
        
        school = School(name=full_name, name_sinhala=short, division="Polonnaruwa Zone", is_active=True)
        db.session.add(school)
        db.session.flush()
        
        user = User(username=username, email=f"{username}@plzone.edu.lk", role='school', school_id=school.id)
        user.set_password('school123')
        db.session.add(user)
        created_count += 1
    
    db.session.commit()
    if created_count:
        print(f"Created {created_count} schools. Default school password: school123")
    print("Seed complete. Total schools:", School.query.count())
