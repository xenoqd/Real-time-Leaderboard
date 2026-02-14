from fastapi import APIRouter, Depends

from backend.core.dependencies.current_user import get_current_user
from backend.services.leaderboard_service import get_top_users, get_user_ranking_info
from backend.models.user import User

leaderboard_router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@leaderboard_router.get("/top")
async def top_users(limit: int = 10):
    return await get_top_users(limit)


@leaderboard_router.get("/rank/{user_id}")
async def my_rank(current_user: User = Depends(get_current_user)):
    return await get_user_ranking_info(current_user.id)
