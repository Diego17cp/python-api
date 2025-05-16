from sqlmodel import Session, select
from app.models.user import User
from app.models.team import Team
from app.models.user_teams import UserTeam

def add_user_to_team(session: Session, user_id: int, team_id: int) -> UserTeam:
    user = session.get(User, user_id)
    team = session.get(Team, team_id)

    if not user or not team:
        return None

    existing = session.exec(
        select(UserTeam).where(UserTeam.user_id == user.id, UserTeam.team_id == team.id)
    ).first()
    if existing:
        return existing
    association = UserTeam(user_id=user.id, team_id=team.id)
    session.add(association)
    session.commit()
    session.refresh(association)
    return association
def remove_user_from_team(session: Session, user_id: int, team_id: int) -> bool:
    user_team = session.exec(
        select(UserTeam).where(UserTeam.user_id == user_id, UserTeam.team_id == team_id)
    ).first()
    if not user_team:
        return False
    session.delete(user_team)
    session.commit()
    return True
def get_user_by_team(session: Session, team_id: int) -> list[User]:
    team = session.get(Team, team_id)
    if not team:
        return []
    return team.members
def get_teams_by_user(session: Session, user_id: int) -> list[Team]:
    user = session.get(User, user_id)
    if not user:
        return []
    return user.teams