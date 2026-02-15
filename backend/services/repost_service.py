from backend.repositories.score_repository import ScoreRepository

from datetime import datetime, timedelta

class ReportService:
    @staticmethod
    async def get_top_players_report(session, start_date, end_date, limit=10):
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=7)
        if not end_date:
            end_date = datetime.utcnow()
        rows = await ScoreRepository.get_top_players(
            session=session,
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )

        return [
            {
                "rank": index + 1,
                "user_id": user_id,
                "total_points": total_points
            }
            for index, (user_id, total_points) in enumerate(rows)
        ]
