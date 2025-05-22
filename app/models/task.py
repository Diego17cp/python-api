import enum 
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from sqlalchemy import Enum as SQLEnum, Column
from datetime import datetime, date
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.board import Board
    from app.models.user import User

class TaskStatus(enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
class Task(Base, table=True):
    __tablename__ = "tasks"
    id: Optional[int] = Field(default=None, primary_key=True)
    board_id: Optional[int] = Field(foreign_key="boards.id", nullable=False)
    title: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    status: TaskStatus = Field(
        sa_column=Column(SQLEnum(TaskStatus, name="task_status"), 
        nullable=False,
        default=TaskStatus.todo)
    )
    assigned_user_id: Optional[int] = Field(foreign_key="users.id", default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    due_date: Optional[date] = Field(default=None)
    board: "Board" = Relationship(back_populates="tasks")
    assigned_user: "User" = Relationship(back_populates="tasks")