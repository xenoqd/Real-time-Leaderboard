from fastapi import APIRouter, Depends
from datetime import datetime

from backend.db.session import get_session
from backend.services.repost_service import ReportService

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

report_router = APIRouter(prefix="/report", tags=["report"])


@report_router.get("/top-players")
async def top_players(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 10,
    session: AsyncSession = Depends(get_session),
):
    report = await ReportService.get_top_players_report(
        session, start_date, end_date, limit
    )
    return report
