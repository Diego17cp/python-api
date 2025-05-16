from typing import List, Optional
from sqlmodel import Field, SQLModel
from app.schemas.team import TeamRead
from app.schemas.task import TaskRead

class BoardBase(SQLModel):
    name: str = Field(nullable=False)
    team_id: int
class BoardCreate(BoardBase):
    pass
class BoardRead(BoardBase):
    id: Optional[int]
    team: Optional[TeamRead]
    tasks: List[TaskRead] = []
