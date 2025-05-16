from sqlmodel import SQLModel, Field

# Crear una clase en lugar de una tabla
class UserTeam(SQLModel, table=True):
    __tablename__ = "user_team"
    
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    team_id: int = Field(foreign_key="teams.id", primary_key=True)