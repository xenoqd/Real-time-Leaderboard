from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from backend.models.user import User


class UserRepository:
    @staticmethod
    async def get_by_username(session: AsyncSession, username: str):
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        return user

    @staticmethod
    async def get_by_user_id(session: AsyncSession, user_id: int):
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        return user

    @staticmethod
    async def create(session: AsyncSession, user: User):
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
