from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud, database, auth

router = APIRouter()

@router.post("/tasks/", response_model=schemas.Task)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(database.get_db),
    current_user=Depends(auth.get_current_user)
):
    return crud.create_task(db, task, user_id=current_user.id)

@router.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(
    db: Session = Depends(database.get_db),
    current_user=Depends(auth.get_current_user)
):
    return crud.get_tasks(db, user_id=current_user.id)
