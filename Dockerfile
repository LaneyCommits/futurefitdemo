FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN python -m venv venv
RUN venv/scripts/activate
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8000

# Run migrations and start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
