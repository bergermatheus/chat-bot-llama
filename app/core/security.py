from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import hashlib
import secrets
from app.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        salt, hash_part = hashed_password.split("$")
        return hash_password(plain_password, salt) == hashed_password
    except:
        return False


def get_password_hash(password: str) -> str:
    return hash_password(password)


def hash_password(password: str, salt: str = None) -> str:
    if salt is None:
        salt = secrets.token_hex(16)

    hash_obj = hashlib.sha256()
    hash_obj.update((password + salt).encode("utf-8"))
    hash_hex = hash_obj.hexdigest()

    return f"{salt}${hash_hex}"


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        return username
    except JWTError:
        return None
