from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.schemas.user import UserCreate, UserRead
from app.schemas.team import TeamRead
from app.controllers.users import create_user, get_user_by_email, get_user, get_all_users
from app.controllers.user_teams import get_teams_by_user
from app.utils.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def api_create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = get_all_users(db)
    if any(u.email == user.email for u in existing_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return create_user(session=db, user_in=user)
@router.get("/", response_model=list[UserRead])
def api_list_users(
    db: Session = Depends(get_db),
):
    users = get_all_users(db)
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found",
        )
    return users
@router.get("/{user_id}", response_model=UserRead)
def api_get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
@router.get("/{user_id}/teams", response_model=list[TeamRead])
def api_get_teams_by_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    teams = get_teams_by_user(db, user_id)
    if not teams:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No teams found for this user",
        )
    return teams