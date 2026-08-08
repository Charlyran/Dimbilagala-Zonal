# Deploy Polonnaruwa Zone Marks System

## Option A – Render.com (free, easiest)

1. Create a GitHub repository and push this folder.
2. Go to https://render.com → Sign up with GitHub
3. New → Web Service → Connect your repo
4. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn run:app --bind 0.0.0.0:$PORT`
   - Environment: Python 3
5. Add environment variable (optional):
   - `SECRET_KEY` = any long random string
6. Deploy → you get a public URL like `https://your-app.onrender.com`

## Option B – Railway.app

1. Push to GitHub
2. https://railway.app → New Project → Deploy from GitHub
3. It auto-detects Python. Add start command if needed:
   `gunicorn run:app --bind 0.0.0.0:$PORT`

## Option C – PythonAnywhere

1. Upload the zip or clone from GitHub
2. Create a Web App (Flask)
3. Point WSGI file to `run:app`

## After deploy

Open the public URL → login:
- Admin: `admin` / `admin123`
- Schools: username / `school123`

**Change the admin password after first login in production.**
