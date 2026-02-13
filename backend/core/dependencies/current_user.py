import jwt
from jwt import PyJWTError
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from backend.core.security.jwt import decode_access_token
from backend.db.session import get_session
from backend.repositories.user_repository import UserRepository


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    auth_cookie: Optional[str] = request.cookies.get("access_token")
    if not auth_cookie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = auth_cookie

    try:
        payload = decode_access_token(token)
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = await UserRepository.get_by_user_id(session, int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user