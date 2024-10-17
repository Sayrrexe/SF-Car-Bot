#!/bin/bash

# Define variables
MEDIA_DIR="media/cars"
IMAGE_NAME="sf-car-bot:latest"  # Replace with your actual image name
DOCKERFILE_PATH="Dockerfile"  # Adjust if your Dockerfile is in a different location
STACK_NAME="bot_stack"

# Step 0: Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Installing Docker..."

    # Update package database
    sudo apt-get update

    # Install required packages
    sudo apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release \
        apt-transport-https

    # Add Docker’s official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    # Set up the stable repository
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    # Update package database again
    sudo apt-get update

    # Install Docker
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io

    # Start Docker service and enable it to start at boot
    sudo systemctl start docker
    sudo systemctl enable docker

    # Add current user to the Docker group to avoid using sudo
    sudo usermod -aG docker $USER

    echo "Docker installed successfully. Please log out and log back in to use Docker without sudo."
    sudo reboot
else
    echo "Docker is already installed."
fi

# Step 1: Create media directory if it doesn't exist
if [ ! -d "$MEDIA_DIR" ]; then
    mkdir -p "$MEDIA_DIR"
    echo "Directory $MEDIA_DIR created."
else
    echo "Directory $MEDIA_DIR already exists."
fi

# Step 2: Build the Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME -f $DOCKERFILE_PATH .

if [ $? -eq 0 ]; then
    echo "Docker image $IMAGE_NAME built successfully."
else
    echo "Error building Docker image."
    exit 1
fi

# Step 3: Check if Docker Swarm is initialized
if ! docker info | grep -q "Swarm: active"; then
    echo "Initializing Docker Swarm..."
    docker swarm init
else
    echo "Docker Swarm is already initialized."
fi

# Step 4: Deploy to Docker Swarm
echo "Deploying to Docker Swarm..."
docker stack deploy -c docker-compose.yml $STACK_NAME

if [ $? -eq 0 ]; then
    echo "Deployment to Docker Swarm completed successfully."
else
    echo "Error deploying to Docker Swarm."
    exit 1
fi

echo "Script completed successfully."
