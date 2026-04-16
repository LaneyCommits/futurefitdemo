# ExploringU

A structured career clarity assessment that maps your thinking patterns to real academic majors and career paths.

## Tech Stack

| Layer    | Technology                                |
|----------|-------------------------------------------|
| Backend  | Django 4.2 + Django REST Framework        |
| Frontend | React 19 + Vite 8                         |
| Database | PostgreSQL (production) / SQLite (dev)    |
| Auth     | Token-based (DRF `authtoken`)             |
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
```

## Quick Start

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

## Docker

```bash
docker compose up
```

- API: `http://localhost:8000`
- Frontend: `http://localhost:5175`

Docker Compose runs migrations and seeds data on startup.

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

See `.env.example` for all options. Key variables:

| Variable             | Default                          | Description              |
|----------------------|----------------------------------|--------------------------|
| `DJANGO_SECRET_KEY`  | insecure fallback                | Django secret key        |
| `DJANGO_DEBUG`       | `True`                           | Debug mode               |
| `DATABASE_URL`       | *(SQLite)*                       | PostgreSQL connection    |
| `ALLOWED_HOSTS`      | `localhost,127.0.0.1,0.0.0.0`   | Extra allowed hosts      |
| `CORS_ALLOWED_ORIGINS` | localhost:5173-5175            | Extra CORS origins       |

## License

Private project.
