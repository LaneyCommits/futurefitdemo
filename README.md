# Student Career Helper

A Django full-stack web app that helps students with **resume gap analysis** (resume vs. job listing) and **career discovery** via a short quiz based on likes, dislikes, and personality.

## Features

- **Resume Gap Analysis** — Paste your resume and a job description to see which skills and requirements are missing so you can tailor your application.
- **Career Discovery Quiz** — Answer 8 questions about your preferences and personality to get personalized career suggestions.

## Setup

### 1. Clone or download the project

```bash
cd Project7
```

### 2. Create and activate a virtual environment

Already created:

```bash
# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

If you need to recreate it:

```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Run the development server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Project structure

```
Project7/
├── config/             # Django project settings
├── resume_analysis/     # Gap analysis app (views, forms, analysis logic)
├── career_quiz/        # Career quiz app (questions, scoring, results)
├── templates/           # Base and app templates
├── static/css/         # Styles
├── manage.py
├── requirements.txt
└── README.md
```

## Pushing to GitHub

1. Create a new repository on GitHub (do not initialize with a README if you already have one).
2. In the project folder:

```bash
git init
git add .
git commit -m "Initial commit: Student Career Helper Django app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

The included `.gitignore` excludes `venv/`, `db.sqlite3`, `__pycache__/`, and other files you typically don’t want in the repo.

## Optional: production settings

For production, set environment variables:

- `DJANGO_SECRET_KEY` — a long random secret key
- `DJANGO_DEBUG=False`
- Add your host to `ALLOWED_HOSTS` in `config/settings.py` or via env

## License

MIT (or your choice).
