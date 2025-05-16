from typing import Optional
from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    email: str = Field(index=True, nullable=False)

class UserCreate(UserBase):
    password: str = Field(min_length=8, nullable=False)
    role: str = Field(default="member", nullable=False)

class UserRead(UserBase):
    id: Optional[int]
    role: str