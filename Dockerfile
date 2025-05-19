# 1. Base image
FROM python:3.9.18-slim

# 2. Prevent .pyc files, force stdout/stderr unbuffered 
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 3. Install dependencies and force Flask <2.3 (to satisfy old Flask-Session)
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && pip install "Flask<2.3"

# 4. Copy your application code
COPY . .

# 5. Ensure the Flask-Session file cache directory exists and is writable
RUN mkdir -p /app/flask_session

# 6. Expose and run
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]