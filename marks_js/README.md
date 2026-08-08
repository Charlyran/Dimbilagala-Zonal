# Polonnaruwa Zone Marks System (JavaScript + Supabase)

No Python needed. Runs in the browser. Database & login = Supabase (free).

## What you get
- Admin zone overview (all 39 schools, progress, averages)
- School login → classes → students → marks entry
- Works on phone & computer browsers
- Deploy free on Netlify / Vercel / GitHub Pages

---

## Setup (about 15 minutes)

### 1. Create Supabase project
1. Go to https://supabase.com → Sign up → **New project**
2. Wait until the project is ready
3. Left menu → **SQL Editor** → New query
4. Copy **all** of `sql/schema.sql` → paste → **Run**
5. Left menu → **Project Settings** → **API**
   - Copy **Project URL**
   - Copy **anon public** key

### 2. Put URL & key in the app
Open `js/config.js` and replace:

```js
const SUPABASE_URL = 'https://xxxx.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOi...';
```

### 3. Create login users
In Supabase:
1. **Authentication** → **Users** → **Add user**
   - Email: `admin@zone.edu.lk`
   - Password: `admin123`
   - Auto Confirm: ON
2. **SQL Editor** – run (replace USER_UUID with the user’s UUID from Auth → Users):

```sql
-- Admin profile (get UUID from Authentication → Users)
INSERT INTO profiles (id, username, role)
VALUES ('PASTE-ADMIN-USER-UUID-HERE', 'admin', 'admin');

-- Example school user: first create Auth user email school1@zone.edu.lk / school123
-- Then link to school id 1 (WILAYAYA):
INSERT INTO profiles (id, username, role, school_id)
VALUES ('PASTE-SCHOOL-USER-UUID-HERE', 'wilayaya', 'school', 1);
```

Repeat for other schools (change school_id).  
School list is in the `schools` table after you ran schema.sql.

### 4. Open the app
- Double-click `index.html`, **or**
- Put the folder on Netlify/Vercel/GitHub Pages for a public link

Login with the emails you created.

---

## Deploy free (public URL for phones)

### Netlify (easiest)
1. https://app.netlify.com → **Add new site** → **Deploy manually**
2. Drag the whole `marks_js` folder
3. You get a link like `https://random-name.netlify.app`

Or connect a GitHub repo and auto-deploy.

### GitHub Pages
1. Push this folder to a GitHub repo
2. Settings → Pages → Deploy from branch `main` / root
3. Open `https://YOUR_USER.github.io/REPO_NAME/`

---

## File structure
```
marks_js/
  index.html      ← Login
  admin.html      ← Zone overall results
  school.html     ← School dashboard
  students.html   ← Add students
  marks.html      ← Enter marks
  js/config.js    ← Your Supabase keys
  js/auth.js
  css/style.css
  sql/schema.sql  ← Run once in Supabase
```

## Notes
- Default admin after you create the user: email + password you set
- Change passwords after first use
- Free Supabase tier is enough for a zonal office
