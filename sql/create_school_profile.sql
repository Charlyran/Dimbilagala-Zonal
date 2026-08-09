-- ============================================
-- CREATE SCHOOL PROFILE (example)
-- ============================================
-- 1. Create Auth user first (e.g. school1@zone.edu.lk / school123)
-- 2. Copy that user's UUID
-- 3. Replace PASTE-UUID-HERE
-- 4. school_id = 1 is WILAYAYA (check: SELECT id, name FROM schools ORDER BY id LIMIT 5;)

INSERT INTO profiles (id, username, role, school_id, full_name)
VALUES (
  'PASTE-UUID-HERE',
  'wilayaya',
  'school',
  1,
  'Wilayaya School User'
)
ON CONFLICT (id) DO UPDATE
  SET username = EXCLUDED.username,
      role = EXCLUDED.role,
      school_id = EXCLUDED.school_id;

SELECT p.username, p.role, s.name AS school
FROM profiles p
LEFT JOIN schools s ON s.id = p.school_id;
