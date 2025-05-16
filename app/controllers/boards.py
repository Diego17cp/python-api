from sqlmodel import Session, select
from app.models.board import Board
from app.schemas.board import BoardCreate

def create_board(session: Session, board_data: BoardCreate) -> Board:
    board = Board(**board_data.model_dump())
    session.add(board)
    session.commit()
    session.refresh(board)
    return board
def get_board(session: Session, board_id: int) -> Board | None:
    return session.get(Board, board_id)
def get_boards_by_team(session: Session, team_id: int) -> list[Board]:
    return session.exec(
        select(Board).where(Board.team_id == team_id)
    ).all()