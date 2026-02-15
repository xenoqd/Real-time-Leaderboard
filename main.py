from fastapi import FastAPI

from backend.services.leaderboard_service import rebuild_leaderboard
from backend.db.session import init_db

from backend.api.v1.leaderboard.leaderboard import leaderboard_router
from backend.api.v1.report.report import report_router
from backend.api.v1.match.match import match_router
from backend.api.v1.score.score import score_router
from backend.api.v1.auth.auth import auth_router


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_db()
    try:
        await rebuild_leaderboard()

    except Exception as e:
        print("Redis unavailable")


app.include_router(auth_router)
app.include_router(match_router)
app.include_router(score_router)
app.include_router(report_router)
app.include_router(leaderboard_router)
