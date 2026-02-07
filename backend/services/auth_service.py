from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.security.jwt import create_access_token, create_refresh_token
from backend.core.security.password import get_password_hash, verify_password
from backend.repositories.user_repository import UserRepository
from backend.core.config import settings
from backend.models.user import User

from fastapi import Response, status
from fastapi.exceptions import HTTPException


class AuthService:
    async def register(
        response: Response,
        session: AsyncSession,
        data
    ):
        existing = await UserRepository.get_by_username(session, data.username)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exist"
            )

        user = User(
            username=data.username,
            hashed_password=get_password_hash(data.password)
        )

        await UserRepository.create(session, user)
        
        access_token = create_access_token(
            {
                "sub": str(user.id),
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": str(user.id),
            }
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            path="/",
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            path="/",
        )
        return user

    async def login(
        response: Response,
        session: AsyncSession,
        data,
    ):
        user = await UserRepository.get_by_username(session, data.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password or login",
            )

        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password or login",
            )
        
        access_token = create_access_token(
            {
                "sub": str(user.id),
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": str(user.id),
            }
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            path="/",
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            path="/",
        )

        return user

