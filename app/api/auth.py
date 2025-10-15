from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.models.conversation import Conversation
from app.models.user import User
from app.schemas.auth import UserLogin, Token
from app.schemas.user import UserCreate
from app.core.security import (
    verify_password,
    create_access_token,
    get_password_hash,
)
from app.config import settings
import uuid

router = APIRouter()


@router.post("/register", response_model=dict)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = (
        db.query(User)
        .filter((User.username == user.username) | (User.email == user.email))
        .first()
    )
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username or email already registered"
        )

    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User created successfully", "user_id": db_user.id}


@router.post("/login", response_model=Token)
async def login_user(
    user_credentials: UserLogin, db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.username == user_credentials.username)
        .first()
    )
    if not user or not verify_password(
        user_credentials.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    session_id = str(uuid.uuid4())
    conversation = Conversation(user_id=user.id, session_id=session_id)
    db.add(conversation)
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "session_id": session_id,
    }
