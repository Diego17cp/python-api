from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from .. import schemas, crud, database, auth
from collections import defaultdict
from datetime import datetime

router = APIRouter()

@router.post("/tasks/", response_model=schemas.Task)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(database.get_db),
    current_user=Depends(auth.get_current_user)
):
    return crud.create_task(db, task, user_id=current_user.id)

@router.get("/", response_model=list[schemas.Task])
def read_tasks(
    db: Session = Depends(database.get_db),
    current_user=Depends(auth.get_current_user)
):
    """
    Devuelve todas las tareas del usuario autenticado.
    """
    return crud.get_tasks(db, user_id=current_user.id)

@router.post("/tasks/group-local")
def group_tasks_local(
    db: Session = Depends(database.get_db),
    current_user=Depends(auth.get_current_user)
):
    """
    Agrupa las tareas del usuario logeado por la primera palabra del título.
    """
    user_tasks = crud.get_tasks(db, user_id=current_user.id)
    grupos = defaultdict(list)
    for task in user_tasks:
        primera_palabra = (task.title.strip().split()[0] if task.title.strip() else "Sin título")
        grupos[primera_palabra].append(task.title)
    return {
        "grupos": [{"nombre": k, "tareas": v} for k, v in grupos.items()],
        "sugerencias": []
    }

@router.post("/tasks/suggest-completion-local")
def suggest_completion_local(
    texto_inicial: str = Body(...),
    max_tokens: int = Body(50),
    language: str = Body("es")
):
    """
    Sugiere cómo completar un texto dado usando reglas simples (no IA).
    """
    completions = [
        " y fomenta la colaboración entre los miembros del equipo.",
        " utilizando herramientas digitales para organizar las tareas.",
        " estableciendo objetivos claros y medibles.",
        " y revisa periódicamente el progreso para mejorar continuamente."
    ]
    # Selecciona una sugerencia simple
    sugerencia = completions[hash(texto_inicial) % len(completions)]
    return {"completacion": texto_inicial.strip() + sugerencia}

@router.get("/tasks/suggest-next")
def suggest_next_tasks(
    db: Session = Depends(database.get_db),
    current_user=Depends(auth.get_current_user)
):
    """
    Devuelve un listado de tareas pendientes ordenadas por la fecha 'completed_at' más cercana a hoy.
    """
    user_tasks = crud.get_tasks(db, user_id=current_user.id)
    pending_tasks = [
        t for t in user_tasks
        if not getattr(t, "completed", False) and getattr(t, "completed_at", None) is not None
    ]
    if not pending_tasks:
        return {"tareas_sugeridas": []}
    hoy = datetime.utcnow()
    pending_tasks.sort(key=lambda t: abs((t.completed_at - hoy).total_seconds()))
    return {
        "tareas_sugeridas": [
            {
                "id": t.id,
                "title": t.title,
                "completed_at": t.completed_at,
                "created_at": t.created_at,
                "description": t.description
            }
            for t in pending_tasks
        ]
    }

@router.get("/tasks/suggest-ia")
def suggest_ia_tasks(
    db: Session = Depends(database.get_db),
    current_user=Depends(auth.get_current_user)
):
    """
    Sugerencia IA local: 
    - Si el usuario tiene muchas tareas pendientes, sugiere priorizar las más antiguas.
    - Si tiene pocas tareas, sugiere agregar nuevas tareas relacionadas a las existentes.
    """
    user_tasks = crud.get_tasks(db, user_id=current_user.id)
    pending_tasks = [
        t for t in user_tasks
        if not getattr(t, "completed", False)
    ]
    sugerencias = []
    if len(pending_tasks) > 5:
        sugerencias.append("Tienes muchas tareas pendientes. Prioriza las más antiguas o divide el trabajo en subtareas.")
    elif len(pending_tasks) == 0:
        sugerencias.append("¡No tienes tareas pendientes! Considera agregar nuevas tareas para avanzar en tus proyectos.")
    else:
        titulos = [t.title for t in pending_tasks]
        if titulos:
            sugerencias.append(f"Considera agregar subtareas relacionadas a: {', '.join(titulos[:2])}.")

    return {
        "sugerencias_ia": sugerencias,
        "total_pendientes": len(pending_tasks)
    }

@router.patch("/tasks/{task_id}/complete")
def complete_task(
    task_id: int,
    db: Session = Depends(database.get_db),
    current_user=Depends(auth.get_current_user)
):
    """
    Marca una tarea como completada y asigna la fecha actual a completed_at.
    """
    task = db.query(crud.models.Task).filter_by(id=task_id, owner_id=current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    if task.completed:
        return {"message": "La tarea ya estaba completada"}
    task.completed = True
    task.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return {"message": "Tarea marcada como completada", "task_id": task.id, "completed_at": task.completed_at}
