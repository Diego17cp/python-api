from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.controllers.tasks import (
    create_task,
    get_task,
    get_tasks_by_board,
    update_task,
    delete_task,
)
from app.utils.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=TaskRead, status_code=201)
def api_create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
):
    return create_task(session=db, task_data=task)
@router.get("/board/{board_id}", response_model=list[TaskRead])
def api_list_tasks(
    board_id: int,
    db: Session = Depends(get_db),
):
    tasks = get_tasks_by_board(db, board_id)
    if not tasks:
        raise HTTPException(
            status_code=404,
            detail="No tasks found for this board",
        )
    return tasks
@router.get("/{task_id}", response_model=TaskRead)
def api_get_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )
    return task
@router.patch("/{task_id}", response_model=TaskRead)
def api_update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
):
    updated_task = update_task(db, task_id, task)
    if not updated_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )
    return updated_task
@router.delete("/{task_id}", status_code=204)
def api_delete_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_task(db, task_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )
    return None