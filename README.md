# Proyecto 1 — Planificación de Tareas
Integrantes:
- Matias Osorio
- Tomas Moya
- Joaquin Gonzalez

## Cómo ejecutar
1. Crear virtual environment: `python -m venv .venv`
2. Activar: `source .venv/bin/activate`
3. Instalar dependencias: `pip install -r requirements.txt`
4. Ejecutar: `python main.py <makespan_objetivo>`



##Funcionamiento del programa

                 ┌─────────────────────────────┐
                 │         Inicio              │
                 └─────────────┬───────────────┘
                               │
                               v
                 ┌─────────────────────────────┐
                 │ Leer tareas.txt y           │
                 │ recursos.txt                │
                 └─────────────┬───────────────┘
                               │
                               v

