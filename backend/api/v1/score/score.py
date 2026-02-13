from fastapi import APIRouter, Depends

from backend.schemas.score import ScoreCreate
from backend.core.dependencies.current_user import get_current_user

from backend.db.session import get_session
from backend.models.user import User
from backend.services.score_service import ScoreService

from sqlalchemy.ext.asyncio import AsyncSession


score_router = APIRouter(prefix="/scores", tags=["scores"])


@score_router.get("/")
async def total_score(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    score = await ScoreService.get_user_total_score(session, user_id, current_user)
    return score