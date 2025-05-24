#!/bin/bash

# Setup script for the Retail Q&A Application
# This script sets up the environment and starts the application

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null || ! command -v docker-compose &> /dev/null; then
    echo "Docker and Docker Compose are required to run this application."
    echo "Please install them and try again."
    exit 1
fi

# Set the OpenRouter API key if provided as an argument
if [ ! -z "$1" ]; then
    export OPENROUTER_API_KEY=$1
    echo "Using provided OpenRouter API key."
else
    echo "No OpenRouter API key provided. The application will use fallback answers."
    echo "To use the Cerebras API, run this script with your API key: ./setup.sh YOUR_API_KEY"
fi

# Build and start the containers
echo "Building and starting the application..."
docker-compose build
docker-compose up -d

# Wait for the services to start
echo "Waiting for services to start..."
sleep 5

# Check if the services are running
if docker-compose ps | grep -q "Up"; then
    echo "Services are running!"
    echo "You can access the application at: http://localhost:3000"
    echo "API health check: http://localhost:5000/api/health"
    echo ""
    echo "To stop the application, run: docker-compose down"
else
    echo "There was an issue starting the services. Please check the logs:"
    echo "docker-compose logs"
fi
