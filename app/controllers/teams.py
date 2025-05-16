from sqlmodel import Session, select
from app.models.team import Team
from app.schemas.team import TeamCreate

def create_team(session: Session, team_data: TeamCreate) -> Team:
    team = Team(**team_data.model_dump())
    session.add(team)
    session.commit()
    session.refresh(team)
    return team
def get_team(session: Session, team_id: int) -> Team | None:
    return session.get(Team, team_id)
def get_all_teams(session: Session) -> list[Team]:
    statement = select(Team)
    results = session.exec(statement)
    return results.all()