# Proyecto 1 — Planificación de Tareas

Integrantes:

- Matias Osorio
- Tomas Moya
- Joaquin Gonzalez

## Cómo ejecutar

1. Crear virtual environment: `python -m venv .venv` Para mc y para Win `.venv\Scripts\Activate.ps1`
2. Activar: `source .venv/bin/activate`
3. Instalar dependencias: `pip install -r requirements.txt`
4. Ejecutar: `python main.py <makespan_objetivo>`



 # Funcionamiento del programa

                 ┌─────────────────────────────┐
                 │         Leer archivos       │
                 └─────────────┬───────────────┘
                               │
                               v
                 ┌─────────────────────────────┐
                 │         Construir           │
                 │       compatibilidad        │
                 └─────────────┬───────────────┘
                               │
                               v
                 ┌─────────────────────────────┐
                 │     Preparar el greedy      │
                 │                             │
                 └─────────────┬───────────────┘
                               │
                               v
                 ┌─────────────────────────────┐
                 │        Crear heaps          │
                 │       por categoria         │
                 │                             │
                 └─────────────┬───────────────┘
                               │
                               v
                 ┌─────────────────────────────┐
                 │                             │
                 │       Ordenar tareas        │
                 │                             │
                 └─────────────┬───────────────┘
                               │
                               v
                 ┌─────────────────────────────┐
                 │                             │
                 │      Asignación greedy      │
                 │                             │
                 └─────────────┬───────────────┘
                               │
                               v
                 ┌─────────────────────────────┐
                 │                             │
                 │        Micro-mejora         │
                 │                             │
                 └─────────────┬───────────────┘
                               │
                 ┌─────────────────────────────┐
                 │                             │
                 │      Construir salida       │
                 │                             │
                 └─────────────┬───────────────┘
                               │
                               v
                 ┌─────────────────────────────┐
                 │                             │
                 │     Guardar e imprimir      │
                 │                             │
                 └─────────────────────────────┘