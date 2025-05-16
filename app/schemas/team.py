from typing import Optional, List
from sqlmodel import Field, SQLModel
from app.schemas.user import UserRead

class TeamBase(SQLModel):
    name: str = Field(nullable=False)
class TeamCreate(TeamBase):
    pass
class TeamRead(TeamBase):
    id: Optional[int]
    members: List[UserRead] = []