# python-api

## Uso del endpoint de IA

Puedes interactuar con la IA enviando una petición POST a `/ia/chat` con un JSON como este:

```json
{
  "prompt": "¿Cuál es la capital de Francia?",
  "max_tokens": 50
}
```

Ejemplo usando `curl`:

```bash
curl -X POST http://localhost:8000/ia/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Dame una idea para un nombre de equipo", "max_tokens": 50}'
```

La respuesta será un JSON con el texto generado por la IA:

```json
{
  "response": "Un buen nombre de equipo podría ser 'Los Innovadores'."
}
```

## IA para agrupar tareas y sugerir mejoras

Envía una petición POST a `/ia/agrupar-tareas` con un JSON así:

```json
{
  "tasks": [
    {"title": "Diseñar login", "description": "Pantalla de acceso de usuarios"},
    {"title": "Crear base de datos", "description": "Definir tablas y relaciones"},
    {"title": "Implementar registro", "description": "Formulario de registro de usuarios"}
  ],
  "language": "es"
}
```

La respuesta será algo como:

```json
{
  "grupos": [
    {
      "nombre": "Usuarios",
      "tareas": [
        "Diseñar login",
        "Implementar registro"
      ]
    },
    {
      "nombre": "Base de datos",
      "tareas": [
        "Crear base de datos"
      ]
    }
  ],
  "sugerencias": [
    "Considera unificar el diseño de login y registro.",
    "Asegúrate de que la base de datos soporte autenticación segura."
  ]
}
```