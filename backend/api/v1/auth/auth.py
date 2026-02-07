from backend.services.auth_service import AuthService
from backend.db.session import get_session
from backend.schemas.user import UserCreate, UserLogin, UserRead

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Response


auth_router = APIRouter(prefix="/auth")


@auth_router.post("/register", response_model=UserRead)
async def register(
    data: UserCreate,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    user = await AuthService.register(response, session, data)
    return user


@auth_router.post("/login", response_model=UserRead)
async def login(
    data: UserLogin,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    user = await AuthService.login(response, session, data)
    return user
