# ExploringU

A structured career clarity assessment that maps your thinking patterns to real academic majors and career paths.

**Live at [exploringu.com](https://exploringu.com)**

## Tech Stack

| Layer    | Technology                                |
|----------|-------------------------------------------|
| Backend  | Django 4.2 + Django REST Framework        |
| Frontend | React 19 + Vite 8                         |
| Database | PostgreSQL (production) / SQLite (dev)    |
| Auth     | Token-based (DRF `authtoken`)             |
| Hosting  | DigitalOcean App Platform                 |
| Styling  | Custom CSS design system (Plus Jakarta Sans, sage color-story) |

## Project Structure

```
config/             Django settings, urls, wsgi
apps/
  quiz/             Questions, choices, scoring engine, result interpretation
  careers/          Personality types, majors, jobs
  users/            Auth, profiles, dashboard
frontend/
  src/
    api/            Centralized API client
    pages/          Landing, Quiz, Results, Login, Register, Dashboard
    components/     Navbar, brand, quiz UI, insight carousel
    hooks/          useAuth, useQuiz, useMediaQuery
.do/app.yaml        DigitalOcean App Platform spec
```

## Local Development

### Prerequisites

- Python 3.10+
- Node.js 18+

### 1. Backend

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # edit as needed
python3 manage.py migrate
python3 manage.py seed_careers
python3 manage.py seed_quiz
python3 manage.py runserver
```

Django API runs at `http://localhost:8000`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Or from the repo root:

```bash
npm install && npm run dev
```

Vite dev server runs at `http://localhost:5175` (not 5173). API calls are proxied to Django automatically.

### Docker (local)

```bash
docker compose up
```

- API: `http://localhost:8000`
- Frontend: `http://localhost:5175`

Docker Compose runs migrations and seeds data on startup.

## Deployment (DigitalOcean App Platform)

### 1. Create a free PostgreSQL database

Sign up at [neon.tech](https://neon.tech) (free tier, 0.5 GB). Copy the connection string.

### 2. Create the app on DigitalOcean

1. Go to **App Platform** > **Create App**
2. Connect your GitHub repo (`LaneyCommits/Exploringu`)
3. DO auto-detects the `Dockerfile` and `.do/app.yaml` spec
4. Set these environment variables in the DO console:

| Variable            | Value                                              |
|---------------------|----------------------------------------------------|
| `DJANGO_SECRET_KEY` | A random 50+ character string (mark as secret)     |
| `DJANGO_DEBUG`      | `False`                                            |
| `DATABASE_URL`      | Your Neon PostgreSQL connection string (mark as secret) |
| `ALLOWED_HOSTS`     | `exploringu.com,www.exploringu.com`                |
| `CORS_ALLOWED_ORIGINS` | `https://exploringu.com,https://www.exploringu.com` |

5. Deploy. The Dockerfile handles everything: build React, install Python deps, collect static files, run migrations, seed data, start Gunicorn.

### 3. Connect your domain

1. In the DO app settings, add `exploringu.com` as a custom domain
2. Update your DNS records as instructed by DO (usually a CNAME)
3. DO provisions SSL automatically

### How it works in production

- **Dockerfile** builds the React SPA and bundles it with Django
- **Gunicorn** serves the Django API at `/api/*`
- **WhiteNoise** serves static assets (favicon, images, JS/CSS bundles)
- **Django catch-all** serves `index.html` for all SPA routes (`/`, `/quiz`, `/results`, etc.)
- Everything runs as a single container on one port

## API Endpoints

| Method | URL                             | Auth     | Description                      |
|--------|---------------------------------|----------|----------------------------------|
| GET    | `/api/quiz/questions/`          | Public   | 10 questions with choices        |
| POST   | `/api/quiz/submit/`             | Public   | Submit answers, get full results |
| GET    | `/api/careers/types/`           | Public   | List personality archetypes      |
| GET    | `/api/careers/recommendations/` | Public   | Majors + jobs for a type         |
| POST   | `/api/users/register/`          | Public   | Create account (username + password) |
| POST   | `/api/users/login/`             | Public   | Authenticate, get token          |
| GET    | `/api/users/me/`                | Token    | Current user profile             |
| GET    | `/api/users/dashboard/`         | Token    | Saved results + history          |

## Quiz System

- Exactly 10 weighted questions, 4 choices each
- Multi-archetype weighted scoring (no frontend scoring)
- 6 personality archetypes: Systems Thinker, Analytical Solver, Creative Builder, People Strategist, Explorer, Impact Visionary
- Results include: personality profile, behavioral insights, thinking style, recommended majors, career directions

## User Flow

1. **Landing** -- start assessment (no signup required)
2. **Quiz** -- 10 guided questions, one at a time
3. **Results** -- full thinking report with personality, majors, careers
4. **Login/Register** -- save results, unlock advanced insights
5. **Dashboard** -- view saved profiles and report history

## Environment Variables

See `.env.example` for all options.

| Variable               | Default                        | Description              |
|------------------------|--------------------------------|--------------------------|
| `DJANGO_SECRET_KEY`    | insecure fallback              | Django secret key        |
| `DJANGO_DEBUG`         | `True`                         | Debug mode               |
| `DATABASE_URL`         | *(SQLite)*                     | PostgreSQL connection    |
| `ALLOWED_HOSTS`        | `localhost,127.0.0.1,0.0.0.0` | Extra allowed hosts      |
| `CORS_ALLOWED_ORIGINS` | localhost:5173-5175            | Extra CORS origins       |
| `SECURE_SSL_REDIRECT`  | `true` (when DEBUG=False)      | HTTPS redirect           |

## License

Private project.
