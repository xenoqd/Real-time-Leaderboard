from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.match_repository import MatchRepository
from backend.services.score_service import ScoreService

from backend.models.match import Match, MatchStatus
from backend.models.user import User
from backend.core.dependencies.current_user import get_current_user

from datetime import datetime
from fastapi import Depends, HTTPException, status

class MatchService:
    @staticmethod
    async def create_open_match(
        session: AsyncSession,
        current_user: User,
    ):

        match = Match(
            player_x_id=current_user.id,
            player_o_id=None,
            status=MatchStatus.waiting,
            winner_id=None
        )

        await MatchRepository.create_match(session, match)

        return match

    @staticmethod
    async def join_open_match(
        session: AsyncSession,
        current_user: User,
        match_id: int
    ):
        match = await MatchRepository.get_match_by_id(session, match_id)
        if not match:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Match not found"
                )
        
        if match.status != MatchStatus.waiting:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot join match. Match is no longer active"
            )

        if match.player_o_id is not None:
            raise HTTPException(
                status_code=status.HTTP_410_GONE,
                detail="Match is already full"
            )

        if match.player_x_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are already the creator of this match"
            )

        match.player_o_id = current_user.id
        match.status = match.status.active

        await MatchRepository.update_match(session, match)

        return match

    @staticmethod
    async def make_move(
        session: AsyncSession,
        match_id: int,
        position: int,
        current_user: User,
    ):
        match = await MatchRepository.get_match_by_id(session, match_id)
        if not match:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Match not found"
                )

        if match.status != MatchStatus.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Game is not active"
            )

        if match.current_turn == "X" and match.player_x_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your turn")
        if match.current_turn == "O" and match.player_o_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your turn")


        if not (0 <= position <= 8):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Position must be between 0 and 8")

        if match.board[position] != "-":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cell already occupied")


        symbol = match.current_turn
        board_list = list(match.board)
        board_list[position] = symbol
        match.board = "".join(board_list)


        match.current_turn = "O" if symbol == "X" else "X"

        match.updated_at = datetime.utcnow()

        winner = MatchService._check_winner(match.board)
        if winner:
            match.status = MatchStatus.finished
            match.winner_id = (
                match.player_x_id if winner == "X" else match.player_o_id
            )
        elif "-" not in match.board:
            match.status = MatchStatus.finished
            match.winner_id = None

        await MatchRepository.update_match(session, match)

        if match.status == MatchStatus.finished:
            if match.winner_id is not None:
                winner_id = match.winner_id
                winner_points = 25
                winner_result = "win"

                loser_id = match.player_x_id if winner_id == match.player_o_id else match.player_o_id
                loser_points = 5
                loser_result = "loss"
            else:
                winner_id = None
                winner_points = 12
                winner_result = "draw"
                loser_id = None
                loser_points = 12
                loser_result = "draw"

            if match.player_x_id:
                if match.player_x_id == winner_id:
                    px_points = winner_points
                    px_result = winner_result
                elif winner_id is None:
                    px_points = 12
                    px_result = "draw"
                else:
                    px_points = 5
                    px_result = "loss"

                await ScoreService.add_points(
                    session=session,
                    user_id=match.player_x_id,
                    points=px_points,
                    match_id=match.id,
                    result=px_result
                )

            if match.player_o_id:
                if match.player_o_id == winner_id:
                    po_points = winner_points
                    po_result = winner_result
                elif winner_id is None:
                    po_points = 12
                    po_result = "draw"
                else:
                    po_points = 5
                    po_result = "loss"

                await ScoreService.add_points(
                    session=session,
                    user_id=match.player_o_id,
                    points=po_points,
                    match_id=match.id,
                    result=po_result
                )

        return {
            "match_id": match.id,
            "board": match.board,
            "current_turn": match.current_turn,
            "status": match.status,
            "winner_id": match.winner_id,
        }

    @staticmethod
    def _check_winner(board: str):
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6),
        ]
        for a, b, c in wins:
            if board[a] == board[b] == board[c] != "-":
                return board[a]
        return None