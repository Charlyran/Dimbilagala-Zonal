-- Run this in Supabase SQL Editor (Dashboard → SQL → New query)

-- Schools
CREATE TABLE IF NOT EXISTS schools (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  name_short TEXT,
  division TEXT DEFAULT 'Polonnaruwa Zone',
  principal_name TEXT,
  contact_phone TEXT,
  contact_email TEXT,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Users (linked to Supabase Auth via auth.users)
CREATE TABLE IF NOT EXISTS profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username TEXT UNIQUE,
  role TEXT NOT NULL CHECK (role IN ('admin', 'school')),
  school_id BIGINT REFERENCES schools(id) ON DELETE SET NULL,
  full_name TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Grades
CREATE TABLE IF NOT EXISTS grades (
  id SERIAL PRIMARY KEY,
  number INT UNIQUE NOT NULL,
  name TEXT,
  name_sinhala TEXT,
  num_subjects INT DEFAULT 6
);

-- Classes (e.g. 6-A)
CREATE TABLE IF NOT EXISTS classes (
  id BIGSERIAL PRIMARY KEY,
  school_id BIGINT NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
  grade_number INT NOT NULL,
  section TEXT NOT NULL,
  class_teacher TEXT,
  UNIQUE(school_id, grade_number, section)
);

-- Students
CREATE TABLE IF NOT EXISTS students (
  id BIGSERIAL PRIMARY KEY,
  school_id BIGINT NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
  class_id BIGINT NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
  admission_no TEXT,
  name TEXT NOT NULL,
  gender TEXT,
  date_of_birth DATE,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Subjects
CREATE TABLE IF NOT EXISTS subjects (
  id SERIAL PRIMARY KEY,
  code TEXT,
  name TEXT NOT NULL,
  name_sinhala TEXT,
  category TEXT DEFAULT 'core',
  is_aesthetic BOOLEAN DEFAULT false,
  grade_from INT DEFAULT 3,
  grade_to INT DEFAULT 13,
  is_active BOOLEAN DEFAULT true
);

-- Terms
CREATE TABLE IF NOT EXISTS terms (
  id SERIAL PRIMARY KEY,
  year INT NOT NULL,
  term_number INT NOT NULL,
  name TEXT,
  is_active BOOLEAN DEFAULT false,
  UNIQUE(year, term_number)
);

-- Marks
CREATE TABLE IF NOT EXISTS marks (
  id BIGSERIAL PRIMARY KEY,
  student_id BIGINT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  subject_id INT NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
  term_id INT NOT NULL REFERENCES terms(id) ON DELETE CASCADE,
  score NUMERIC(5,2),
  is_absent BOOLEAN DEFAULT false,
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(student_id, subject_id, term_id)
);

-- Enable RLS
ALTER TABLE schools ENABLE ROW LEVEL SECURITY;
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE classes ENABLE ROW LEVEL SECURITY;
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE terms ENABLE ROW LEVEL SECURITY;
ALTER TABLE marks ENABLE ROW LEVEL SECURITY;
ALTER TABLE grades ENABLE ROW LEVEL SECURITY;

-- Simple policies: authenticated users can read; write based on role (simplified for start)
CREATE POLICY "Public read schools" ON schools FOR SELECT TO authenticated USING (true);
CREATE POLICY "Admin write schools" ON schools FOR ALL TO authenticated
  USING (EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin'));

CREATE POLICY "Read own profile" ON profiles FOR SELECT TO authenticated USING (true);
CREATE POLICY "Update own profile" ON profiles FOR UPDATE TO authenticated USING (id = auth.uid());

CREATE POLICY "Read classes" ON classes FOR SELECT TO authenticated USING (true);
CREATE POLICY "Write classes" ON classes FOR ALL TO authenticated USING (true);

CREATE POLICY "Read students" ON students FOR SELECT TO authenticated USING (true);
CREATE POLICY "Write students" ON students FOR ALL TO authenticated USING (true);

CREATE POLICY "Read subjects" ON subjects FOR SELECT TO authenticated USING (true);
CREATE POLICY "Read terms" ON terms FOR SELECT TO authenticated USING (true);
CREATE POLICY "Write terms" ON terms FOR ALL TO authenticated
  USING (EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin'));

CREATE POLICY "Read marks" ON marks FOR SELECT TO authenticated USING (true);
CREATE POLICY "Write marks" ON marks FOR ALL TO authenticated USING (true);

CREATE POLICY "Read grades" ON grades FOR SELECT TO authenticated USING (true);

-- Seed grades
INSERT INTO grades (number, name, name_sinhala, num_subjects) VALUES
(3,'Grade 3','3 ශ්‍රේණිය',6),(4,'Grade 4','4 ශ්‍රේණිය',6),(5,'Grade 5','5 ශ්‍රේණිය',6),
(6,'Grade 6','6 ශ්‍රේණිය',12),(7,'Grade 7','7 ශ්‍රේණිය',12),(8,'Grade 8','8 ශ්‍රේණිය',12),
(9,'Grade 9','9 ශ්‍රේණිය',12),(10,'Grade 10','10 ශ්‍රේණිය',9),(11,'Grade 11','11 ශ්‍රේණිය',9),
(12,'Grade 12','12 ශ්‍රේණිය',4),(13,'Grade 13','13 ශ්‍රේණිය',4)
ON CONFLICT (number) DO NOTHING;

-- Seed term
INSERT INTO terms (year, term_number, name, is_active)
VALUES (2026, 2, 'II වාර පරීක්ෂණය - 2026', true)
ON CONFLICT (year, term_number) DO NOTHING;

-- Seed subjects
INSERT INTO subjects (code, name, name_sinhala, category, is_aesthetic, grade_from, grade_to) VALUES
('1','Mother Tongue','මව් බස','core',false,3,13),
('2','Religion','ආගම','religion',false,3,13),
('3','English','ඉංග්‍රිසි','core',false,3,13),
('4','Mathematics','ගණිතය','core',false,3,13),
('5','Science','විද්‍යාව','core',false,6,11),
('6','History','ඉතිහාසය','core',false,6,11),
('7','Geography','භූගෝල විද්‍යාව','core',false,6,11),
('8','Civic Education','පුරවැසි අධ්‍යාපනය','core',false,6,11),
('9','Second Language','දෙවන බස','core',false,6,11),
('10','Health & PE','සෞඛ්‍ය හා ශාරීරික අධ්‍යාපනය','core',false,6,11),
('11','Practical Skills','ප්‍රායෝගික හා තාක්ෂණික කුසලතා','core',false,6,9),
('12','Music','සංගීත(පෙ)','aesthetic',true,6,11),
('13','Art','චිත්‍ර','aesthetic',true,6,11),
('14','Dancing','නැටුම්(දේශිය)','aesthetic',true,6,11),
('15','Drama','රංග කලාව','aesthetic',true,6,11),
('16','ICT','ICT','core',false,6,11)
ON CONFLICT DO NOTHING;

-- 39 Polonnaruwa schools
INSERT INTO schools (name, name_short, division) VALUES
('PL/WILAYAYA MADHYA MAHA VIDYALAYA','WILAYAYA MADHYA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/SIRIPURA MADHYA MAHA VIDYALAYA','SIRIPURA MADHYA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/WELIKANDA MAHA VIDYALAYA','WELIKANDA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/WEHERAGALA MAHA VIDYALAYA','WEHERAGALA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/MEDAGAMA MAHA VIDYALAYA','MEDAGAMA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/SEVANAPITIYA MAHA VIDYALAYA','SEVANAPITIYA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/NIKAWATHALANDA MAHA VIDYALAYA','NIKAWATHALANDA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/BOGASWEWA MAHA VIDYALAYA','BOGASWEWA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/LEELARATHNA WIJESINGHA MAHA VIDYALAYA','LEELARATHNA WIJESINGHA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/ELLEWEWA MAHA VIDYALAYA','ELLEWEWA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/ASELAPURA MAHA VIDYALAYA','ASELAPURA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/NUWARAGALA MAHA VIDYALAYA','NUWARAGALA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/ALAWAKUMBURA MAHA VIDYALAYA','ALAWAKUMBURA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/NELUMWEWA MAHA VIDYALAYA','NELUMWEWA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/MADURU OYA MAHA VIDYALAYA','MADURU OYA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/MANAMPITIYA SINHALA MAHA VIDYALAYA','MANAMPITIYA SINHALA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/KASHYAPA MAHA VIDYALAYA','KASHYAPA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/VIJAYA PARAKKRAMA KANISHTA VIDYALAYA','VIJAYA PARAKKRAMA KANISHTA VIDYALAYA','Polonnaruwa Zone'),
('PL/DAMMINNA MAHA VIDYALAYA','DAMMINNA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/SINHAPURA KANISTA VIDYALAYA','SINHAPURA KANISTA VIDYALAYA','Polonnaruwa Zone'),
('PL/PIHITIWEWA MAHA VIDYALAYA','PIHITIWEWA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/KALINGAWILA KANISHTA VIDYALAYA','KALINGAWILA KANISHTA VIDYALAYA','Polonnaruwa Zone'),
('PL/KADAWATHAMADUWA DHARMAPALA KANISHTA VIDYALAYA','KADAWATHAMADUWA DHARMAPALA KANISHTA VIDYALAYA','Polonnaruwa Zone'),
('PL/BANDANAGALA KANISHTA VIDYALAYA','BANDANAGALA KANISHTA VIDYALAYA','Polonnaruwa Zone'),
('PL/KANDEGAMA KANISHTA VIDYALAYA','KANDEGAMA KANISHTA VIDYALAYA','Polonnaruwa Zone'),
('PL/PAHALA YAKKURE KANISHTA VIDYALAYA','PAHALA YAKKURE KANISHTA VIDYALAYA','Polonnaruwa Zone'),
('PL/PELATIYAWEWA SECONDARY SCHOOL','PELATIYAWEWA SECONDARY SCHOOL','Polonnaruwa Zone'),
('PL/KEKULUWELA MAHA VIDYALAYA','KEKULUWELA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/NAWAPALLEGAMA VIDYALAYA','NAWAPALLEGAMA VIDYALAYA','Polonnaruwa Zone'),
('PL/NAWAGINIDAMANA MAHA VIDYALAYA','NAWAGINIDAMANA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/IHALA YAKKURE KANISHTA VIDYALAYA','IHALA YAKKURE KANISHTA VIDYALAYA','Polonnaruwa Zone'),
('PL/MAGULDAMANA MAHA VIDYALAYA','MAGULDAMANA MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/KATUWANWILA MUSLIM KANISHTA VIDYALAYA','KATUWANWILA MUSLIM KANISHTA VIDYALAYA','Polonnaruwa Zone'),
('PL/SENAPURA AL AMEEN MUSLIM MAHA VIDYALAYA','SENAPURA AL AMEEN MUSLIM MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/MANAMPITIYA TAMIL MAHA VIDYALAYA','MANAMPITIYA TAMIL MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/HEWANPITIYA TAMIL MAHA VIDYALAYA','HEWANPITIYA TAMIL MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/MUTUGALA TAMIL VIDYALAYA','MUTUGALA TAMIL VIDYALAYA','Polonnaruwa Zone'),
('PL/THRIKONAMADUWA MUSLIM MAHA VIDYALAYA','THRIKONAMADUWA MUSLIM MAHA VIDYALAYA','Polonnaruwa Zone'),
('PL/ROTAWEWA TAMIL KANISHTA VIDYALAYA','ROTAWEWA TAMIL KANISHTA VIDYALAYA','Polonnaruwa Zone')
ON CONFLICT (name) DO NOTHING;
