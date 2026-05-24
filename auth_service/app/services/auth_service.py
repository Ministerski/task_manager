from datetime import datetime, timezone, timedelta
from typing import List, Optional

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.core.config import settings
from app.core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token,
)
from app.models.models import User, LoginHistory
from app.schemas.auth import (
    RegisterRequest, LoginRequest, UpdateUserRequest,
    TokenResponse, UserResponse, LoginHistoryResponse,
)


class AuthService:

    @staticmethod
    def register(session: Session, data: RegisterRequest) -> UserResponse:
        existing = session.exec(
            select(User).where(User.email == data.email)
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered.",
            )
        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return UserResponse(id=user.id, email=user.email)

    @staticmethod
    def login(
        session: Session,
        data: LoginRequest,
        user_agent: Optional[str] = None,
    ) -> TokenResponse:
        user = session.exec(
            select(User).where(User.email == data.email)
        ).first()
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        # Save login history
        history = LoginHistory(
            user_id=user.id,
            user_agent=user_agent,
            logged_at=datetime.now(timezone.utc),
        )
        session.add(history)
        session.commit()

        return TokenResponse(
            access_token=create_access_token(str(user.id)),
            refresh_token=create_refresh_token(str(user.id)),
        )

    @staticmethod
    def refresh(refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token.",
            )
        user_id = payload.get("sub")
        return TokenResponse(
            access_token=create_access_token(user_id),
            refresh_token=create_refresh_token(user_id),
        )

    @staticmethod
    def update_user(
        session: Session,
        user: User,
        data: UpdateUserRequest,
    ) -> UserResponse:
        if not data.email and not data.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Provide email or password to update.",
            )
        if data.email:
            existing = session.exec(
                select(User).where(User.email == data.email)
            ).first()
            if existing and existing.id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already in use.",
                )
            user.email = data.email
        if data.password:
            user.hashed_password = hash_password(data.password)

        session.add(user)
        session.commit()
        session.refresh(user)
        return UserResponse(id=user.id, email=user.email)

    @staticmethod
    def get_history(session: Session, user: User) -> List[LoginHistoryResponse]:
        records = session.exec(
            select(LoginHistory)
            .where(LoginHistory.user_id == user.id)
            .order_by(LoginHistory.logged_at.desc())
        ).all()
        return [
            LoginHistoryResponse(
                id=r.id,
                user_agent=r.user_agent,
                datetime=r.logged_at.isoformat(),
            )
            for r in records
        ]

    @staticmethod
    def logout(token: str, redis) -> dict:
        if redis is None:
            # Redis not available — just return ok
            return {"detail": "Logged out successfully."}

        payload = decode_token(token)
        if payload:
            exp = payload.get("exp")
            if exp:
                ttl = int(exp - datetime.now(timezone.utc).timestamp())
                if ttl > 0:
                    redis.setex(f"blacklist:{token}", ttl, "1")

        return {"detail": "Logged out successfully."}
