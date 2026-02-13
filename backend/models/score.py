from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class GameResult(str, Enum):
    win = "win"
    lose = "loss"
    draw = "draw"


class Score(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id")
    match_id: int = Field(foreign_key="match.id")

    points: int
    result: GameResult

    created_at: datetime = Field(default_factory=datetime.utcnow)
