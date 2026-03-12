# ExploringU

**Campus to career.** Career quiz, resume templates, gap analysis, and college finder—all free for students.

![ExploringU homepage](docs/images/homepage-screenshot.png)

## Features

| Feature | Description |
|---------|-------------|
| **Career Quiz** | Short quiz by major or explore mode; personalized job suggestions |
| **Resume Templates** | Major-specific resumes, cover letters, admissions essays + FutureBot AI |
| **Gap Analysis** | Paste resume + job posting → AI match score, missing keywords, suggestions |
| **College Finder** | Filter by major, location, cost, school type |

## TODO:
- [ ] Add ability to make futurebot popup larger 
- [ ] Make resume tips section into carousel 
- [ ] Add more colleges 
- [ ] Finish sign-in functionality so users can save resumes
    - [ ] optional: make it so verification emails are sent to the user
    - [ ] add profile pictures
- [ ] consider adding mbti test
- [ ] add ability to download resumes/resume templates as docx
- [ ] add way for AI chat to reference user behavior
- [ ] add way to search for jobs by major
    - maybe using serpapi?
- [ ] change dockerfile to use actual server instead of debug server
    - possibly using gunicorn
    - [https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu#step-6-testing-gunicorn-s-ability-to-serve-the-project](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu#step-6-testing-gunicorn-s-ability-to-serve-the-project)

## Quick Start

```bash
docker compose up --build
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

**AI features** (gap analysis, FutureBot): add `GEMINI_API_KEY` to a `.env` file. Get a key from [Google AI Studio](https://aistudio.google.com/apikey).

**Email verification**: By default, verification emails are not sent to your inbox—they are printed in the terminal where you run `runserver`. To receive real emails, set SMTP variables in `.env` (see "Email" in `config/settings.py`); for Gmail, use an [App Password](https://support.google.com/accounts/answer/185833).

## Local Setup

```bash
cd ExploringU
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## GitHub Pages

Static preview in `docs/`. Deploy: **Settings → Pages** → source `main` / folder `docs`. Full app: use Docker.

## Structure

```
ExploringU/
├── config/           # Django settings
├── resume_analysis/  # Gap analysis
├── career_quiz/      # Quiz
├── resume/           # Templates, cover letters, essays
├── schools/          # College finder
├── docs/             # Static site
├── templates/
└── static/
```

## License

MIT
