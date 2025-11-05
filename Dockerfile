# Use official Python 3.11.0 slim image (specific version for SSL compatibility)
FROM python:3.11.0-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install ca-certificates for SSL
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy CA certificate first
COPY cacert.pem /app/cacert.pem

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run migrations and start Gunicorn server
# Increased timeout to 120s to handle slow email connections
CMD python manage.py migrate && gunicorn covu_soon.wsgi:application --bind 0.0.0.0:8000 --timeout 120 --workers 2
