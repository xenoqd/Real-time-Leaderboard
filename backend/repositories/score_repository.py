from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from backend.models.score import Score
from sqlalchemy import func, desc

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

    @staticmethod
    async def get_top_players(
        session: AsyncSession,
        start_date,
        end_date,
        limit: int = 10
        ):
        result = await session.execute(
            select(
                Score.user_id,
                func.sum(Score.points).label("total_points")
            )
            .where(Score.created_at >= start_date)
            .where(Score.created_at <= end_date)
            .group_by(Score.user_id)
            .order_by(desc("total_points"))
            .limit(limit)
        )

        return result.all()