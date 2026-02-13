from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from backend.models.match import Match


class MatchRepository:
    @staticmethod
    async def create_match(session: AsyncSession, match: Match):
        session.add(match)
        await session.commit()
        await session.refresh(match)
        return match

    @staticmethod
    async def get_match_by_id(session: AsyncSession, match_id: int):
        query = select(Match).where(Match.id == match_id)
        result = await session.execute(query)
        match = result.scalar_one_or_none()
        return match

    @staticmethod
    async def update_match(session: AsyncSession, match: Match):
        await session.commit()
        await session.refresh(match)
