# Use a multi-stage build to keep the final image small
FROM python:3.13-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.13-slim

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

# Set the working directory
WORKDIR /home/app/web

# Install dependencies from the builder stage
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy the application code
COPY . .

# Change ownership of the files
RUN chown -R app:app /home/app/web

# Switch to the non-root user
USER app

# Expose the port
EXPOSE 8000

# Run collectstatic
RUN python manage.py collectstatic --noinput

# Run the application with Gunicorn
CMD gunicorn celio.wsgi:application --bind 0.0.0.0:$PORT
