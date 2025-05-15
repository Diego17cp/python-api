from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    completed: bool
    owner_id: int
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True
