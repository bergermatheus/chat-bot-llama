# Chat API with Authentication

A FastAPI-based chat application with user authentication and conversation history using Ollama, with a React frontend.

## Features

- User registration and authentication with JWT tokens
- Chat with AI using Ollama (phi3:mini model)
- Conversation history storage
- React frontend
- RESTful API endpoints
- Docker support

## Quick Start

### Using Docker Compose

1. **Run the setup script:**
```bash
chmod +x setup.sh
./setup.sh
```

2. **Access the application:**
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Manual Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Start Ollama:**
```bash
docker run -d -p 11434:11434 --name ollama ollama/ollama
docker exec ollama ollama pull phi3:mini
```

3. **Run the application:**
```bash
uvicorn app.main:app --reload
```

## Docker Commands

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose stop

# Restart a service
docker-compose restart frontend

# View logs
docker-compose logs -f

# Rebuild and start
docker-compose up --build
```

## API Endpoints

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/agent/chat` - Send chat message
- `GET /api/v1/chatagent/conversation/history` - Get conversation history
- `DELETE /api/v1/agent/conversation/clear` - Clear conversation
- `GET /api/v1/users/me` - Get current user info

## Frontend Features

- User registration and login
- Real-time chat interface
- Conversation history sidebar