# FutureFit

**FutureFit** is a Django web app that helps students get from campus to career. *You don't have to know yet* — discover careers that fit your personality with a short quiz, explore majors and roles, and take the next step.

## Features

- **Resume Gap Analysis** — Paste your resume and a job description (or a job type like "Database Administrator") to see gaps and get AI tailoring and ATS tips.
- **Career Discovery Quiz** — Take a short quiz by major or explore majors and careers; get personalized job suggestions.

## Setup

### 1. Clone or download the project

```bash
cd FutureFit
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

### 6. (Optional) AI resume tools — Gemini API key

For “Review my resume” and other AI features, add a Gemini API key to a `.env` file in the project root:

- **Use a key from [Google AI Studio](https://aistudio.google.com/apikey)** (create one there).  
- Do **not** use a key from Google Cloud Console; that will give “API keys are not supported” and requires OAuth.

In `.env`:

```
GEMINI_API_KEY=your-key-from-aistudio-google-com
```

## Run on GitHub Pages (static site)

FutureFit includes a **static version** in the `docs/` folder that runs entirely in the browser—no server needed. To host it on GitHub Pages:

1. Push your repo to GitHub.
2. Go to **Settings → Pages** in your repository.
3. Under **Source**, choose **Deploy from a branch**.
4. Select branch **main** and folder **/ (root)** or **/docs**.
   - If you choose **/docs**, the site is built from the `docs/` folder.
5. Click **Save**. Your site will be live at `https://YOUR_USERNAME.github.io/FutureFit/` in a few minutes.

To update the quiz data before deploying, run:

```bash
python3 scripts/export_quiz_json.py > docs/js/quiz-data.json
```

## Project structure

```
FutureFit/
├── config/             # Django project settings
├── resume_analysis/     # Gap analysis app (views, forms, analysis logic)
├── career_quiz/        # Career quiz app (questions, scoring, results)
├── docs/               # Static site for GitHub Pages (quiz, home, about)
├── templates/          # Base and app templates
├── static/css/         # Styles
├── scripts/            # export_quiz_json.py for static site data
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
git commit -m "Initial commit: FutureFit Django app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/FutureFit.git
git push -u origin main
```

The included `.gitignore` excludes `venv/`, `db.sqlite3`, `__pycache__/`, and other files you typically don’t want in the repo.



## License

MIT (or your choice).
