ARG BASE=nvidia/cuda:11.8.0-base-ubuntu22.04
FROM ${BASE}

# Set the working directory in the container
WORKDIR /usr/src/app

RUN apt-get update && apt-get upgrade -y
# Install necessary system dependencies
RUN apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    python3-wheel \
    espeak-ng \
    libsndfile1-dev \
    portaudio19-dev \
    libasound2-dev \
    && rm -rf /var/lib/apt/lists/*
    
RUN pip3 install llvmlite --ignore-installed

# Install FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg screen && \
    rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /data
RUN mkdir /data/audio_cache

# Make port 5001 available to the world outside this container
EXPOSE 5011

# Define environment variable
ENV NAME World

# Make the script executable
RUN chmod +x /usr/src/app/start.sh

# Run the script when the container starts
CMD ["./start.sh"]
