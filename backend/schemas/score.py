from pydantic import BaseModel
from backend.models.score import GameResult

class ScoreCreate(BaseModel):
    match_id: int
    points: int
    result: GameResult