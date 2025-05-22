from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.team import Team
    from app.models.task import Task

class Board(Base, table=True):
    __tablename__ = "boards"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    team_id: Optional[int] = Field(foreign_key="teams.id", nullable=False)
    team: "Team" = Relationship(back_populates="boards")
    tasks: List["Task"] = Relationship(back_populates="board")