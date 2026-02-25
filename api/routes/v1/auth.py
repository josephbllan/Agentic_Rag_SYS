from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from api.security.jwt_handler import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    oauth2_scheme,
)
from api.schemas.user import User
from api.schemas.token import Token
from api.schemas.user_response import UserResponse
from api.security.token_blacklist import blacklist
from config.settings import JWT_CONFIG

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticates a user with username and password credentials
    and returns a bearer access token on success.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token(
        {"sub": user.username, "roles": user.roles},
        timedelta(minutes=JWT_CONFIG["access_token_expire_minutes"]),
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": JWT_CONFIG["access_token_expire_minutes"] * 60,
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
):
    """Returns profile information for the currently authenticated user
    including username, email, full name, and assigned roles.
    """
    return UserResponse(
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        roles=current_user.roles,
    )


@router.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme),
    current_user: User = Depends(get_current_active_user),
):
    """Logs out the current user by revoking their access token
    and adding it to the in-memory blacklist.
    """
    blacklist.revoke(token)
    return {"message": f"User {current_user.username} logged out successfully"}
