# ExploringU

A structured career clarity assessment that maps your thinking patterns to real academic majors and career paths.

- **Live:** [exploringu.com](https://exploringu.com)
- **Source:** [github.com/LaneyCommits/exploringu](https://github.com/LaneyCommits/exploringu)

## Tech stack

| Layer    | Technology                                |
|----------|-------------------------------------------|
| Backend  | Django 4.2 + Django REST Framework        |
| Frontend | React 19 + Vite 8 |
| Database | PostgreSQL (production) / SQLite (local)  |
| Auth     | Token-based (DRF `authtoken`)             |
| Hosting  | DigitalOcean App Platform (Dockerfile)    |
| Styling  | Custom CSS design system (Plus Jakarta Sans, sage palette) |

## Project structure

```
config/             Django settings, URLs, WSGI
apps/
  quiz/             Questions, choices, scoring, results
  careers/          Personality types, majors, jobs
  users/            Auth, profiles, dashboard
frontend/
  src/
    api/            API client
    pages/          Landing, quiz, results, login, register, dashboard
    components/     Navbar, brand, quiz UI, insight carousel
    hooks/          useAuth, useQuiz, useMediaQuery
.do/app.yaml        DigitalOcean App Platform spec (optional)
Dockerfile          Production image: build SPA → Gunicorn + WhiteNoise
docker-compose.yml  Local dev: Django `runserver` + Vite dev server
```

## Local development

### Prerequisites

- **Python 3.11+** (matches the production Docker image)
- **Node.js 18+** (20.x is used in Docker)

### 1. Backend

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env # edit as needed
python3 manage.py migrate
python3 manage.py seed_careers
python3 manage.py seed_quiz
python3 manage.py runserver
```

Django runs at [http://127.0.0.1:8000](http://127.0.0.1:8000).

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

Vite serves the app at [http://localhost:5175](http://localhost:5175) (see `frontend/vite.config.js`). API requests are proxied to Django when you use the dev server.

### Docker (local)

```bash
docker compose up --build
```

- **API:** [http://127.0.0.1:8000](http://127.0.0.1:8000) — `migrate`, `seed_careers`, and `seed_quiz` run on the API container startup.
- **Frontend:** [http://localhost:5175](http://localhost:5175) — Vite inside Docker uses `VITE_API_PROXY_TARGET=http://api:8000` so the proxy hits the Compose service name, not `localhost`.

## Deployment (DigitalOcean App Platform)

### 1. PostgreSQL database

Use any managed Postgres (e.g. [Neon](https://neon.tech)) and copy the connection string for `DATABASE_URL`.

### 2. Create the app

1. In **App Platform**, choose **Create App** and connect GitHub.
2. Select repo **`LaneyCommits/exploringu`**, branch **`main`**.
3. DigitalOcean can build from the **`Dockerfile`**; you can optionally use the checked-in **`.do/app.yaml`** as a starting spec.
4. Set **HTTP port** to **8080** (the `Dockerfile` exposes this; Gunicorn binds `0.0.0.0:${PORT:-8080}`).

### 3. Environment variables

| Variable                 | Value |
|--------------------------|--------|
| `DJANGO_SECRET_KEY`      | Random 50+ characters (**secret**) |
| `DJANGO_DEBUG`           | `False` |
| `DATABASE_URL`           | Postgres URL (**secret**) |
| `ALLOWED_HOSTS`        | `exploringu.com,www.exploringu.com` (comma-separated) |
| `CORS_ALLOWED_ORIGINS` | `https://exploringu.com,https://www.exploringu.com` |
| `SECURE_SSL_REDIRECT`    | `true` (default when `DEBUG=False`; see `.env.example`) |

On deploy, the container runs migrations, seeds careers/quiz data, then starts Gunicorn.

### 4. Custom domain

Add your domain in the app settings, point DNS as DigitalOcean instructs (often a CNAME), and TLS is provisioned automatically.

### How production is served

- **Multi-stage `Dockerfile`:** `npm ci` / `npm run build` for the React app, then copy `frontend/dist` into the Python image.
- **Gunicorn** serves Django; **`/api/*`** and **`/admin/`** are handled by Django.
- **WhiteNoise** serves static assets from the Vite build.
- **SPA fallback:** unmatched paths return `frontend/dist/index.html` so client-side routes work.

## API endpoints

| Method | URL                             | Auth | Description |
|--------|----------------------------------|--------|-------------|
| GET    | `/api/quiz/questions/`           | Public | Quiz questions and choices |
| POST   | `/api/quiz/submit/`            | Public | Submit answers, get results |
| GET    | `/api/careers/types/`            | Public | Personality archetypes |
| GET    | `/api/careers/recommendations/` | Public | Majors and jobs for a type |
| POST   | `/api/users/register/`         | Public | Register (username + password) |
| POST   | `/api/users/login/`            | Public | Login, returns token |
| GET    | `/api/users/me/`               | Token  | Current user |
| GET    | `/api/users/dashboard/`        | Token  | Saved results / history |

## Quiz system

- Ten weighted questions, four choices each.
- Server-side multi-archetype scoring (no client-side scoring logic).
- Six archetypes: Systems Thinker, Analytical Solver, Creative Builder, People Strategist, Explorer, Impact Visionary.
- Results include profile copy, behavioral insights, thinking style, majors, and career directions.

## User flow

1. **Landing** — start the assessment (no account required).
2. **Quiz** — ten steps, one question at a time.
3. **Results** — full report with personality, majors, and careers.
4. **Register / login** — save results and use the dashboard.
5. **Dashboard** — saved profiles and history.

## Environment variables

Copy **`.env.example`** to **`.env`** for local development.

| Variable               | Default (local) | Description |
|------------------------|-------------------|-------------|
| `DJANGO_SECRET_KEY`    | Dev fallback      | Django secret |
| `DJANGO_DEBUG`         | `True`            | Debug mode |
| `DATABASE_URL`         | *(empty → SQLite)* | Postgres DSN |
| `ALLOWED_HOSTS`        | *(see settings)*  | Extra hosts, comma-separated |
| `CORS_ALLOWED_ORIGINS` | *(see settings)*  | Extra origins, comma-separated |
| `SECURE_SSL_REDIRECT`  | `true` when `DEBUG=False` | Redirect HTTP→HTTPS |

## License

Private project.
