from fastapi import APIRouter, Depends

from backend.core.dependencies.current_user import get_current_user
from backend.services.match_service import MatchService
from backend.db.session import get_session
from backend.models.user import User

from sqlalchemy.ext.asyncio import AsyncSession


match_router = APIRouter(prefix="/matches", tags=["match"])


@match_router.post("/")
async def create_open_match(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    match = await MatchService.create_open_match(session, current_user)
    return match


@match_router.post("/{match_id}/join")
async def join_match(
    match_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    match = await MatchService.join_open_match(session, current_user, match_id)
    return match


@match_router.post("/{match_id}/move")
async def move(
    match_id: int,
    position: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    match = await MatchService.make_move(session, match_id, position, current_user)
    return match
