from sqlmodel import SQLModel, Field, Column, String
from typing import Optional
from datetime import datetime
from enum import Enum


class MatchStatus(str, Enum):
    waiting = "waiting"
    active = "active"
    finished = "finished"


class Match(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    player_x_id: int = Field(foreign_key="user.id")
    player_o_id: Optional[int] = Field(foreign_key="user.id")

    winner_id: Optional[int] = None
    status: MatchStatus

    board: str = Field(
        sa_column=Column(String(9), default="---------", nullable=False)
    )
    current_turn: str = Field(default="X")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None, nullable=True)
