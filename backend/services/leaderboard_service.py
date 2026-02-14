from backend.infrastructure.redis.client import redis_client
from backend.core.config import settings
from backend.db.session import get_session_factory

from backend.models.score import Score

from sqlalchemy import select, func

LEADERBOARD_KEY = "leaderboard:global"


async def update_score(user_id: int, points: int):
    await redis_client.zincrby(
        LEADERBOARD_KEY,
        points,
        user_id,
    )


async def get_top_users(limit: int = 10):
    results = await redis_client.zrevrange(
        LEADERBOARD_KEY, 0, limit - 1, withscores=True
    )

    leaderboard = []

    for index, (user_id, score) in enumerate(results, start=1):
        leaderboard.append(
            {"rank": index, "user_id": int(user_id), "score": int(score)}
        )

    return leaderboard


async def get_user_ranking_info(user_id: int):
    rank = await redis_client.zrevrank(LEADERBOARD_KEY, user_id)

    if rank is None:
        return None

    score = await redis_client.zscore(LEADERBOARD_KEY, user_id)

    return {"user_id": user_id, "rank": rank + 1, "score": score}


async def rebuild_leaderboard():
    factory = get_session_factory()
    async with factory() as session:

        result = await session.execute(
            select(
                Score.user_id,
                func.sum(Score.points).label("total_points")
            ).group_by(Score.user_id)
        )
        
        rows = result.all()

        await redis_client.delete(LEADERBOARD_KEY)

        if rows: 
            mapping = {str(user_id): float(total) for user_id, total in rows}

            await redis_client.zadd(LEADERBOARD_KEY, mapping)
