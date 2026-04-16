# Multi-stage build: React frontend + Django API

# --- Stage 1: Build React frontend ---
FROM node:20-slim AS frontend-build
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# --- Stage 2: Django API + static frontend ---
FROM python:3.11-slim-bookworm
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .
COPY --from=frontend-build /frontend/dist /app/frontend/dist

RUN DJANGO_SECRET_KEY=collect-static-only \
    DJANGO_DEBUG=False \
    python manage.py collectstatic --noinput 2>/dev/null || true

EXPOSE 8080

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py seed_careers && python manage.py seed_quiz && exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 2 --threads 2 --timeout 120"]
