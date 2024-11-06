# Use a specific Python version as the base image
FROM python:3.10.3-slim-bullseye

# Install system dependencies
RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

# Clone and install dlib (used by face_recognition)
RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS

# Set the working directory to your Flask app
WORKDIR /root/backend_for_smart_attendance_system

# Copy your app into the container
COPY . /root/backend_for_smart_attendance_system

# Install dependencies from requirements.txt
RUN pip3 install -r requirements.txt

# Install the face_recognition package itself
RUN python3 setup.py install

# Command to run your Flask app (adjust if needed)
CMD ["python3", "app.py"]
