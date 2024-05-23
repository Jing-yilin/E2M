# Use the official Python image from the Docker Hub
FROM python:3.10-slim

LABEL maintainer="yilin.jing.ai@outlook.com"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install\
    libgl1\
    libgl1-mesa-glx \ 
    libglib2.0-0 -y && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# production stage
ENV FLASK_ENV=production
ENV API_URL=http://localhost:8765
ENV CONVERTER=default

# set time zone
ENV TZ=Asia/Shanghai

# Expose the port that the app runs on
EXPOSE 8765

# Run the Flask application
CMD ["gunicorn", "--bind", "0.0.0.0:8765", "app:create_app()"]