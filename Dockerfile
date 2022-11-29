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
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . .