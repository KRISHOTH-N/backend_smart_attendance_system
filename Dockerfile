# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set environment variables to prevent Python from writing pyc files and buffer output
ENV PYTHONUNBUFFERED=1

# Install system dependencies, including build tools and cmake
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    g++ \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . /app/

# Expose the port that the Flask app will run on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
