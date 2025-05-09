# 1. Base image (explicit tag)
FROM python:3.9.18-slim

# 2. Prevent .pyc files, force stdout/stderr unbuffered 
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Create a non‑root user
RUN adduser --disabled-password appuser

WORKDIR /app

# 4. Install dependencies first (leverages Docker layer cache)
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 5. Copy app code
COPY . .

# 6. Change ownership so appuser can read/write (e.g. SQLite file in instance/)
RUN chown -R appuser:appuser /app

USER appuser

# 7. Expose the port the app runs on
EXPOSE 5000

# 8. Use Gunicorn for production‑grade WSGI serving
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
