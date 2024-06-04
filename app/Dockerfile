# Use the official Python image from the Docker Hub
FROM python:3.10-slim

LABEL maintainer="yilin.jing.ai@outlook.com"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    mupdf \
    libmupdf-dev \
    libreoffice \
    libgl1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port that the app runs on
EXPOSE 8765

# RUN chmod +x run_docker.sh
RUN chmod +x setup_db_docker.sh

# Define entrypoint to run setup script and start the application
ENTRYPOINT ["/bin/sh", "-c", "./setup_db_docker.sh && exec gunicorn --bind 0.0.0.0:8765 --timeout 500 app:app"]



