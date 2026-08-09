-- SAFE re-run script for Supabase
-- Run this if you already ran schema.sql once and got policy errors

-- Drop existing policies (ignore errors if missing)
DO $$ BEGIN
  DROP POLICY IF EXISTS "Public read schools" ON schools;
  DROP POLICY IF EXISTS "Admin write schools" ON schools;
  DROP POLICY IF EXISTS "Read own profile" ON profiles;
  DROP POLICY IF EXISTS "Update own profile" ON profiles;
  DROP POLICY IF EXISTS "Read classes" ON classes;
  DROP POLICY IF EXISTS "Write classes" ON classes;
  DROP POLICY IF EXISTS "Read students" ON students;
  DROP POLICY IF EXISTS "Write students" ON students;
  DROP POLICY IF EXISTS "Read subjects" ON subjects;
  DROP POLICY IF EXISTS "Read terms" ON terms;
  DROP POLICY IF EXISTS "Write terms" ON terms;
  DROP POLICY IF EXISTS "Read marks" ON marks;
  DROP POLICY IF EXISTS "Write marks" ON marks;
  DROP POLICY IF EXISTS "Read grades" ON grades;
EXCEPTION WHEN undefined_table THEN NULL;
END $$;

-- Enable RLS (safe if already on)
DO $$ BEGIN
  ALTER TABLE schools ENABLE ROW LEVEL SECURITY;
  ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
  ALTER TABLE classes ENABLE ROW LEVEL SECURITY;
  ALTER TABLE students ENABLE ROW LEVEL SECURITY;
  ALTER TABLE subjects ENABLE ROW LEVEL SECURITY;
  ALTER TABLE terms ENABLE ROW LEVEL SECURITY;
  ALTER TABLE marks ENABLE ROW LEVEL SECURITY;
  ALTER TABLE grades ENABLE ROW LEVEL SECURITY;
EXCEPTION WHEN undefined_table THEN
  RAISE NOTICE 'Some tables missing - run full schema first';
END $$;

-- Recreate policies
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

-- Allow INSERT on profiles for setup (admin linking users)
DROP POLICY IF EXISTS "Insert profiles" ON profiles;
CREATE POLICY "Insert profiles" ON profiles FOR INSERT TO authenticated WITH CHECK (true);
