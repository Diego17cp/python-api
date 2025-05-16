from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.schemas.team import TeamCreate, TeamRead
from app.schemas.user import UserRead
from app.utils.dependencies import get_db
from app.controllers.teams import create_team, get_team, get_all_teams
from app.controllers.user_teams import add_user_to_team, remove_user_from_team, get_user_by_team

router = APIRouter()
# Rutas para la gestión de equipos
@router.post("/", response_model=TeamRead, status_code=201)
def api_create_team(team: TeamCreate,db: Session = Depends(get_db),):
    return create_team(session=db, team_data=team)
@router.get("/", response_model=list[TeamRead])
def api_list_teams(db: Session = Depends(get_db),):
    teams = get_all_teams(db)
    if not teams:
        raise HTTPException(
            status_code=404,
            detail="No teams found",
        )
    return teams
@router.get("/{team_id}", response_model=TeamRead)
def api_get_team(team_id: int, db: Session = Depends(get_db),):
    team = get_team(db, team_id)
    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not found",
        )
    return team
# Rutas para la gestión de usuarios en equipos
@router.post("/{team_id}/users/{user_id}", status_code=status.HTTP_201_CREATED)
def api_add_user_to_team(team_id: int, user_id: int, db: Session = Depends(get_db),):
    association = add_user_to_team(db, user_id, team_id)
    if not association:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User or team not found",
        )
    return {"message": "User added to team successfully"}
def api_remove_user_from_team(team_id: int, user_id: int, db: Session = Depends(get_db),):
    success = remove_user_from_team(db, user_id, team_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User or team not found, or user is not in team",
        )
    return {"message": "User removed from team successfully"}
@router.get("/{team_id}/users", response_model=list[UserRead])
def api_get_users_by_team(team_id: int, db: Session = Depends(get_db),):
    team = get_team(db, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )
    users = get_user_by_team(db, team_id)
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found in this team",
        )
    return users