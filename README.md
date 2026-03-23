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



 # Funcionamiento del programa

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
                 ┌─────────────────────────────┐
                 │ Construir compatibilidades  │
                 │ tarea → recursos válidos    │
                 └─────────────┬───────────────┘
                               │
                               v
                 ┌─────────────────────────────┐
                 │ Ordenar tareas              │
                 │ 1. menos compatibles        │
                 │ 2. mayor duración           │
                 └─────────────┬───────────────┘
                               │
                               v
                 ┌─────────────────────────────┐
                 │ Construcción inicial        │
                 │ Asignar cada tarea al       │
                 │ recurso que minimiza carga  │
                 └─────────────┬───────────────┘
                               │
                               v
                 ┌─────────────────────────────┐
                 │ Mejora local                │
                 │ - mover tareas              │
                 │ - intercambiar tareas       │
                 │ - reordenar dentro          │
                 │   del recurso               │
                 └─────────────┬───────────────┘
                 ┌─────────────────────────────┐
                 │ Verificar solución          │
                 │ - compatibilidad            │
                 │ - no solapamiento           │
                 │ - completitud               │
                 │ - tiempos válidos           │
                 └─────────────┬───────────────┘
                               │
                     ¿solución válida?
                        /           \\
                      no             sí
                      |               |
                      v               v
          ┌──────────────────┐   ┌──────────────────────┐
          │ Reportar error   │   │ Escribir output.txt  │
          └──────────────────┘   └──────────┬───────────┘
                                            │
                                            v
                                 ┌────────────────────────┐
                                 │ Calcular makespan y    │
                                 │ tiempo de ejecución    │
                                 └──────────┬─────────────┘
                                            │
                                            v
                                 ┌────────────────────────┐
                                 │          Fin           │
                                 └────────────────────────┘