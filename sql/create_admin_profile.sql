-- ============================================
-- CREATE ADMIN PROFILE
-- ============================================
-- 1. Go to Authentication → Users
-- 2. Copy the UUID of admin@zone.edu.lk (or your admin user)
-- 3. Replace PASTE-UUID-HERE below with that UUID
-- 4. Run this query

INSERT INTO profiles (id, username, role, full_name)
VALUES (
  'PASTE-UUID-HERE',   -- e.g. a1b2c3d4-e5f6-7890-abcd-ef1234567890
  'admin',
  'admin',
  'Zonal Admin'
)
ON CONFLICT (id) DO UPDATE
  SET username = EXCLUDED.username,
      role = EXCLUDED.role,
      full_name = EXCLUDED.full_name;

-- Check it worked:
SELECT * FROM profiles;
