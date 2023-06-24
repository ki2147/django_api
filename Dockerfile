FROM ubuntu:latest

# Install system dependencies
RUN apt-get update \
    && apt-get install -y python3 python3-pip python3-venv \
       libmysqlclient-dev build-essential libssl-dev libffi-dev \
       pkg-config nginx

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . /app/

# Create and activate the virtual environment
RUN python3 -m venv productapp_venv
RUN /bin/bash -c "source productapp_venv/bin/activate"

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/sites-available/default

# Collect static files
RUN python3 manage.py collectstatic --noinput

# Update Nginx configuration
RUN sed -i 's|/var/www/html|/app/static|g' /etc/nginx/sites-available/default

# Expose the application port
EXPOSE 80

# Start Nginx and the Django app
CMD service nginx start && gunicorn productapi.wsgi:application --bind 0.0.0.0:8000
