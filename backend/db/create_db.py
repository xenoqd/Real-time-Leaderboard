from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from backend.core.config import settings


async def create_database_if_not_exists():
    admin_url = (
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
        f"{settings.POSTGRES_PASSWORD}@{settings.DB_HOST}:"
        f"{settings.DB_PORT}/postgres"
    )

    engine = create_async_engine(admin_url, isolation_level="AUTOCOMMIT")

    async with engine.connect() as conn:
        result = await conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
            {"dbname": settings.POSTGRES_DB},
        )

        db_exists = result.scalar() is not None

        if not db_exists:
            await conn.execute(text(f'CREATE DATABASE "{settings.POSTGRES_DB}"'))
        else:
            print(f"Database {settings.POSTGRES_DB} already exist.")

    await engine.dispose()
