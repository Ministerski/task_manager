from typing import List
from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from app.core.dependencies import get_current_user
from app.db.database import get_session
from app.db.redis_client import get_redis
from app.models.models import User
from app.schemas.auth import (
    RegisterRequest, LoginRequest, RefreshRequest,
    UpdateUserRequest, TokenResponse, UserResponse, LoginHistoryResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(tags=["Auth"])
bearer = HTTPBearer()


@router.post("/register", response_model=UserResponse, status_code=201)
def register(
    data: RegisterRequest,
    session: Session = Depends(get_session),
):
    """Регистрация нового пользователя."""
    return AuthService.register(session, data)


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    request: Request,
    session: Session = Depends(get_session),
):
    """Аутентификация пользователя, возвращает access и refresh токены."""
    user_agent = request.headers.get("user-agent")
    return AuthService.login(session, data, user_agent)


@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshRequest):
    """Обновление access токена с помощью refresh токена."""
    return AuthService.refresh(data.refresh_token)


@router.put("/user/update", response_model=UserResponse)
def update_user(
    data: UpdateUserRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Обновление email или пароля авторизованного пользователя."""
    return AuthService.update_user(session, current_user, data)


@router.get("/user/history", response_model=List[LoginHistoryResponse])
def get_history(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """История входов авторизованного пользователя."""
    return AuthService.get_history(session, current_user)


@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    current_user: User = Depends(get_current_user),
    redis=Depends(get_redis),
):
    """Выход из системы — добавляет токен в чёрный список Redis."""
    return AuthService.logout(credentials.credentials, redis)
