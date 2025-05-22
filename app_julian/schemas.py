from pydantic import BaseModel
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: str = None
    created_at: datetime = None
    completed_at: datetime = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    completed: bool
    owner_id: int
    class Config:
        from_attributes = True  # <- Usar esto en vez de orm_mode para Pydantic v2

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes = True  # <- Usar esto en vez de orm_mode para Pydantic v2

# Puedes agregar modelos para los endpoints de IA si lo deseas.
