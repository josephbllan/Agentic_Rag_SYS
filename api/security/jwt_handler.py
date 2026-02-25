from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from config.settings import JWT_CONFIG, DEMO_USERS
from .password_handler import verify_password
from .token_blacklist import blacklist
from api.schemas.user import User
from api.schemas.user_in_db import UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=JWT_CONFIG["access_token_expire_minutes"]))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_CONFIG["secret_key"], algorithm=JWT_CONFIG["algorithm"])


def get_user(username: str) -> Optional[UserInDB]:
    if username in DEMO_USERS:
        return UserInDB(**DEMO_USERS[username])
    return None


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    user = get_user(username)
    return user if user and verify_password(password, user.hashed_password) else None


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    if blacklist.is_revoked(token):
        raise HTTPException(status_code=401, detail="Token has been revoked")
    try:
        payload = jwt.decode(token, JWT_CONFIG["secret_key"], algorithms=[JWT_CONFIG["algorithm"]])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user(username)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return User(**user.model_dump())
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
