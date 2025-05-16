import enum
from typing import Optional
from datetime import datetime, date
from sqlmodel import Field, SQLModel
from app.schemas.user import UserRead

class TaskStatus(str, enum.Enum):
    todo="todo"
    in_progress="in_progress"
    done="done"
class TaskBase(SQLModel):
    title: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    status: TaskStatus = Field(default=TaskStatus.todo)
    due_date: Optional[date] = Field(default=None)
    assigned_user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    board_id: int
class TaskCreate(TaskBase):
    pass
class TaskRead(TaskBase):
    id: Optional[int]
    created_at: datetime
class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[date] = None
    assigned_user_id: Optional[int] = None