from sqlmodel import Field, SQLModel

class Token(SQLModel):
    access_token: str 
    token_type: str = Field(default="bearer")