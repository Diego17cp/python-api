from fastapi import FastAPI
from .routes import users, tasks

app = FastAPI(
    title="App Julian API",
    description="API para gestión de usuarios y tareas con agrupación y sugerencias locales.",
    version="1.0.0"
)

# Incluye los endpoints de autenticación y registro en el prefijo raíz
app.include_router(users.router, tags=["users"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de App Julian"}
