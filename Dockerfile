FROM python:3.12-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Node.js and npm
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Debugging Node.js and npm installation
RUN node -v && npm -v

# Install Python dependencies
WORKDIR /app
COPY . /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set NPM_BIN_PATH explicitly in Django settings
ENV NPM_BIN_PATH=/usr/bin/npm

# Install Tailwind CSS and related dependencies
WORKDIR /app/siperpus
RUN npm install
RUN npm i -D daisyui@latest
RUN python manage.py tailwind install
# RUN python manage.py collectstatic --noinput
RUN python manage.py tailwind build


# Expose port
EXPOSE 8082

# Start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8082"]
