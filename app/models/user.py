from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from app.db.base import Base
from app.models.task import Task
from app.models.user_teams import UserTeam

if TYPE_CHECKING:
    from app.models.team import Team

class User(Base, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, nullable=False, unique=True)
    hashed_pw: str = Field(nullable=False)
    role: str = Field(default="member", nullable=False)
    
    teams: List["Team"] = Relationship(
        back_populates="members",
        link_model=UserTeam,
    )
    
    tasks: List[Task] = Relationship(
        back_populates="assigned_user"
    )