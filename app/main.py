from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.api import auth, chat, users


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="A chat API with authentication using Ollama",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
app.include_router(
    auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["authentication"]
)
app.include_router(
    chat.router, prefix=f"{settings.API_V1_STR}/agent", tags=["chat"]
)
app.include_router(
    users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"]
)


@app.get("/")
async def root():
    return {"message": "Welcome to Chat API with Authentication"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
