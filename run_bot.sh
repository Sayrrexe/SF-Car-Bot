#!/bin/bash

# Define variables
MEDIA_DIR="media/cars"
IMAGE_NAME="sf-car-bot:latest"  # Replace with your actual image name
DOCKERFILE_PATH="Dockerfile"  # Adjust if your Dockerfile is in a different location

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

# Step 3: Deploy to Docker Swarm
echo "Deploying to Docker Swarm..."
docker swarm init
docker stack deploy -c docker-compose.yml car_bot_stack

if [ $? -eq 0 ]; then
    echo "Deployment to Docker Swarm completed successfully."
else
    echo "Error deploying to Docker Swarm."
    exit 1
fi

echo "Script completed successfully."
