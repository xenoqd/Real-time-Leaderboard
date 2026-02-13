from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from backend.models.score import Score
from sqlalchemy import func

class ScoreRepository:
    @staticmethod
    async def get_user_score(session: AsyncSession, user_id):
        query = select(func.sum(Score.points)).where(
            Score.user_id == user_id
        )
        result = await session.execute(query)
        total_points = result.scalar()
        return total_points

    @staticmethod
    async def update_score(session: AsyncSession, score: Score):
        session.add(score)
        await session.commit()
        await session.refresh(score)
        return score