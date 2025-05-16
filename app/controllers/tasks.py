from sqlmodel import Session, select
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

def create_task(session: Session, task_data: TaskCreate) -> Task:
    task = Task(**task_data.model_dump())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
def get_task(session: Session, task_id: int) -> Task | None:
    return session.get(Task, task_id)
def get_tasks_by_board(session: Session, board_id: int) -> list[Task]:
    return session.exec(
        select(Task).where(Task.board_id == board_id)
    ).all()
def update_task(session: Session, task_id: int, task_data: TaskUpdate) -> Task | None:
    task = session.get(Task, task_id)
    if task:
        for key, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        session.commit()
        session.refresh(task)
    return task
def delete_task(session: Session, task_id: int) -> bool:
    task = session.get(Task, task_id)
    if task:
        session.delete(task)
        session.commit()
        return True
    return False