# Pull base image
FROM --platform=linux/amd64 python:3.10.4-slim-bullseye

# Set environment variables
# Disable automatic check for pip updates
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
# Don't write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Console ouput not buffered by Docker
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/code

# Install dependencies
#RUN apt-get update \
#    && apt-get install -f -y postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 8080

# Run the web service on container startup
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 config.wsgi:application
