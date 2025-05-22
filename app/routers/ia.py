from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import openai
from app.core.config import settings

router = APIRouter()

class IARequest(BaseModel):
    prompt: str
    max_tokens: int = 100

class TaskItem(BaseModel):
    title: str
    description: str = ""

class GroupTasksRequest(BaseModel):
    tasks: List[TaskItem]
    language: str = "es"  # Idioma de la respuesta

@router.post("/chat")
async def ia_chat(request: IARequest):
    try:
        openai.api_key = settings.SECRET_KEY  # O usa una variable OPENAI_API_KEY en settings
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": request.prompt}],
            max_tokens=request.max_tokens,
        )
        return {"response": response.choices[0].message["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agrupar-tareas")
async def agrupar_tareas_ia(request: GroupTasksRequest):
    try:
        openai.api_key = settings.OPENAI_API_KEY
        prompt = (
            f"Agrupa las siguientes tareas por temática o similitud y sugiere mejoras o agrupaciones útiles para un equipo. "
            f"Responde en {request.language}. Devuelve el resultado en formato JSON con dos claves: 'grupos' (lista de grupos, cada uno con 'nombre' y 'tareas') y 'sugerencias' (lista de sugerencias).\n\n"
            f"Tareas:\n"
        )
        for idx, task in enumerate(request.tasks, 1):
            prompt += f"{idx}. {task.title}: {task.description}\n"
        prompt += "\nEjemplo de respuesta:\n" \
                  "{'grupos': [{'nombre': 'Frontend', 'tareas': [...]}, ...], 'sugerencias': ['...']}\n"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.5,
        )
        # Intentar extraer el JSON de la respuesta
        import json, re
        content = response.choices[0].message["content"]
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            result = json.loads(match.group(0).replace("'", '"'))
            return result
        return {"raw_response": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
