from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from app.db.base import Base
from app.models.board import Board
from app.models.user_teams import UserTeam

if TYPE_CHECKING:
    from app.models.user import User

class Team(Base, table=True):
    __tablename__ = "teams"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True)
    
    members: List["User"] = Relationship(
        back_populates="teams",
        link_model=UserTeam,
    )
    
    boards: List[Board] = Relationship(
        back_populates="team"
    )