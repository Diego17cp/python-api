from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.schemas.board import BoardCreate, BoardRead
from app.controllers.boards import create_board, get_board, get_boards_by_team
from app.utils.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=BoardRead, status_code=201)
def api_create_board(board: BoardCreate,db: Session = Depends(get_db)):
    return create_board(session=db, board_data=board)
@router.get("/team/{team_id}", response_model=list[BoardRead])
def api_list_boards(team_id: int, db: Session = Depends(get_db)):
    boards = get_boards_by_team(db, team_id)
    if not boards:
        raise HTTPException(
            status_code=404,
            detail="No boards found for this team",
        )
    return boards
@router.get("/{board_id}", response_model=BoardRead)
def api_get_board(board_id: int, db: Session = Depends(get_db)):
    board = get_board(db, board_id)
    if not board:
        raise HTTPException(
            status_code=404,
            detail="Board not found",
        )
    return board