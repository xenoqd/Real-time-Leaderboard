from backend.infrastructure.redis.client import redis_client
from backend.core.config import settings

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
            {
                "rank": index, 
                "user_id": int(user_id), 
                "score": int(score)
            }
        )

    return leaderboard


async def get_user_ranking_info(user_id: int):
    rank = await redis_client.zrevrank(LEADERBOARD_KEY, user_id)

    if rank is None:
        return None

    score = await redis_client.zscore(LEADERBOARD_KEY, user_id)

    return {
        "user_id": user_id, 
        "rank": rank + 1, 
        "score": score
        }
