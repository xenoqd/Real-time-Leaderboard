from sqlalchemy.ext.asyncio import AsyncSession

from backend.services.leaderboard_service import update_score
from backend.repositories.score_repository import ScoreRepository
from backend.models.user import User
from backend.models.score import Score, GameResult

from datetime import datetime


class ScoreService:
    @staticmethod
    async def get_user_total_score(
        session: AsyncSession,
        user_id: int,
        current_user: User,
    ):
        score = await ScoreRepository.get_user_score(session, user_id)

        return score

    @staticmethod
    async def add_points(
        session: AsyncSession,
        user_id: int,
        points: int,
        match_id: int,
        result: GameResult,
    ):
        score = Score(
            user_id=user_id,
            points=points,
            result=result,
            match_id=match_id,
        )
        score.created_at = datetime.utcnow()

        await update_score(user_id, points)

        return await ScoreRepository.update_score(session, score)
