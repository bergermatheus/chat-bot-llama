#!/bin/bash
echo "Setting up Chat Application with Docker Compose..."

# Create necessary directories
mkdir -p data

# Set permissions
chmod +x setup.sh

# Pull Ollama model
echo "Pulling Ollama model..."
docker compose up -d ollama
sleep 10
docker exec chat-ollama ollama pull phi3:mini

# Start all services
echo "Starting all services..."
docker compose up -d

echo "Setup complete!"
echo "Frontend: http://localhost:3000"
echo "FastAPI: http://localhost:8000"
echo "Ollama: http://localhost:11434"