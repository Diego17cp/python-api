from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, users, teams, boards, tasks
from app.routers import ia
from app.core.config import settings

app = FastAPI(
    title="Task Management API",
    description="API for managing tasks, boards, teams, and users.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(teams.router, prefix="/teams", tags=["teams"])
app.include_router(boards.router, prefix="/boards", tags=["boards"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(ia.router, prefix="/ia", tags=["ia"])
@app.get("/")
async def root():
    return {"message": "Welcome to the Task Management API!"}