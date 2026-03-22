from __future__ import annotations

import csv
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
#from_future_import annotations es para permitir usar tipos como List[Task] sin necesidad de importarlos antes, lo que ayuda a evitar problemas de importación circular y mejora la legibilidad del código.
#Importamos csv para leer y escribir archivos CSV, sys para acceder a argumentos de línea de comandos, time para medir el tiempo de ejecución, dataclass para definir clases de datos de manera concisa, Path para manejar rutas de archivos, y varios tipos de typing para anotaciones de tipos.

@dataclass(frozen=True)
class Task:
    task_id: str
    duration: int
    category: str
#Dataclass es un decorador que se utiliza para crear clases de datos de manera más sencilla. En este caso, Task representa una tarea con un identificador, duración y categoría. El parámetro frozen=True hace que las instancias de esta clase sean inmutables, lo que significa que sus atributos no pueden ser modificados después de la creación.
#Task tiene tres atributos: task_id (un string que identifica la tarea), duration (un entero que representa la duración de la tarea) y category (un string que indica la categoría a la que pertenece la tarea).
@dataclass(frozen=True)
class Resource:
    resource_id: str
    categories: frozenset[str]
#Resource representa un recurso con un identificador y un conjunto de categorías que puede manejar. Al igual que Task, es inmutable.

@dataclass(frozen=True)
class Assignment:
    task_id: str
    resource_id: str
    start: int
    end: int
#Assignment representa la asignación de una tarea a un recurso, con un tiempo de inicio y fin. También es inmutable.

def read_tasks(file_path: Path) -> List[Task]:
    tasks: List[Task] = []
    with file_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            task_id = row[0].strip()
            duration = int(row[1].strip())
            category = row[2].strip()
            tasks.append(Task(task_id, duration, category))
    return tasks
#Read_tasks lee un archivo CSV de tareas y devuelve una lista de objetos Task. Cada fila del archivo debe contener el identificador de la tarea, su duración y su categoría. El método utiliza csv.reader para leer el archivo y crea instancias de Task a partir de cada fila, que luego se agregan a la lista tasks.
#For row in reader: itera sobre cada fila del archivo CSV. Si la fila está vacía, se omite. Luego, se extraen los valores de task_id, duration y category de la fila, se limpian de espacios en blanco y se crean objetos Task que se agregan a la lista tasks.
#If not row es una verificación para asegurarse de que no se procesen filas vacías, lo que podría causar errores al intentar acceder a índices que no existen.
#Entonces, el archivo es un formulario en filas. Cada fila es una tarea.La función lee cada formulario, separa campos, crea el objeto y guarda en lista. Al final te devuelve el “inventario” de tareas para usar en el algoritmo.

def read_resources(file_path: Path) -> List[Resource]:
    resources: List[Resource] = []
    with file_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            resource_id = row[0].strip()
            categories = frozenset(cell.strip() for cell in row[1:] if cell.strip())
            resources.append(Resource(resource_id, categories))
    return resources
#Read_resources lee un archivo CSV de recursos y devuelve una lista de objetos Resource. Cada fila del archivo debe contener el identificador del recurso seguido de las categorías que puede manejar. El método utiliza csv.reader para leer el archivo y crea instancias de Resource a partir de cada fila, que luego se agregan a la lista resources.


def build_compatibility(
    tasks: List[Task], resources: List[Resource]
) -> Tuple[Dict[str, Task], Dict[str, Resource], Dict[str, List[str]]]:
    task_map: Dict[str, Task] = {t.task_id: t for t in tasks}
    resource_map: Dict[str, Resource] = {r.resource_id: r for r in resources}

    compatible_resources: Dict[str, List[str]] = {}
    for task in tasks:
        compatibles = [
            r.resource_id for r in resources if task.category in r.categories
        ]
        compatible_resources[task.task_id] = compatibles

    return task_map, resource_map, compatible_resources
# Esta función calcula la carga total de trabajo por recurso.

def build_schedule_from_resource_tasks(
    resource_to_tasks: Dict[str, List[str]],
    task_map: Dict[str, Task],
) -> List[Assignment]:
    assignments: List[Assignment] = []

    for resource_id, task_ids in resource_to_tasks.items():
        current_time = 0
        for task_id in task_ids:
            duration = task_map[task_id].duration
            start = current_time
            end = start + duration
            assignments.append(Assignment(task_id, resource_id, start, end))
            current_time = end

    return assignments
# - Para cada recurso, suma la duración de todas las tareas que tiene asignadas.

def compute_resource_loads(
    resource_to_tasks: Dict[str, List[str]],
    task_map: Dict[str, Task],
) -> Dict[str, int]:
    loads: Dict[str, int] = {}
    for resource_id, task_ids in resource_to_tasks.items():
        loads[resource_id] = sum(task_map[task_id].duration for task_id in task_ids)
    return loads
# - Genera un diccionario donde la clave es el ID del recurso

def compute_makespan_from_loads(loads: Dict[str, int]) -> int:
    if not loads:
        return 0
    return max(loads.values())
#   y el valor es el tiempo total de trabajo (carga).

def compute_makespan(assignments: List[Assignment]) -> int:
    if not assignments:
        return 0
    return max(a.end for a in assignments)
# Esto permite analizar qué recursos están más ocupados.

def verify_solution(
    tasks: List[Task],
    resources: List[Resource],
    assignments: List[Assignment],
) -> bool:
    task_map: Dict[str, Task] = {t.task_id: t for t in tasks}
    resource_map: Dict[str, Resource] = {r.resource_id: r for r in resources}

    if len(assignments) != len(tasks):
        return False

    seen_tasks: Set[str] = set()
    by_resource: Dict[str, List[Assignment]] = {}

    for a in assignments:
        if a.task_id in seen_tasks:
            return False
        seen_tasks.add(a.task_id)

        if a.task_id not in task_map or a.resource_id not in resource_map:
            return False

        if a.start < 0 or a.end <= a.start:
            return False

        task = task_map[a.task_id]
        resource = resource_map[a.resource_id]

        if task.category not in resource.categories:
            return False

        by_resource.setdefault(a.resource_id, []).append(a)

    for resource_id, resource_assignments in by_resource.items():
        resource_assignments.sort(key=lambda x: x.start)
        current_end = 0
        for a in resource_assignments:
            if a.start < current_end:
                return False
            if a.end - a.start != task_map[a.task_id].duration:
                return False
            current_end = a.end

    return seen_tasks == set(task_map.keys())


def write_output(file_path: Path, assignments: List[Assignment]) -> None:
    ordered = sorted(assignments, key=lambda a: a.task_id)
    with file_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for a in ordered:
            writer.writerow([a.task_id, a.resource_id, a.start, a.end])


def initial_solution(
    tasks: List[Task],
    resources: List[Resource],
    compatible_resources: Dict[str, List[str]],
    resource_map: Dict[str, Resource],
) -> Dict[str, List[str]]:
    """
    Heurística inicial:
    - tareas más restrictivas primero (menos recursos compatibles)
    - luego mayor duración
    - en empate de recurso, elegir el que deje menor carga final
    - preferir recursos menos flexibles para preservar los más versátiles
    """
    resource_to_tasks: Dict[str, List[str]] = {r.resource_id: [] for r in resources}
    loads: Dict[str, int] = {r.resource_id: 0 for r in resources}
    flexibility: Dict[str, int] = {
        r.resource_id: len(r.categories) for r in resources
    }

    ordered_tasks = sorted(
        tasks,
        key=lambda t: (
            len(compatible_resources[t.task_id]),
            -t.duration,
            t.task_id,
        ),
    )

    for task in ordered_tasks:
        compatibles = compatible_resources[task.task_id]

        best_resource: Optional[str] = None
        best_key: Optional[Tuple[int, int, str]] = None

        for resource_id in compatibles:
            final_load = loads[resource_id] + task.duration
            key = (final_load, flexibility[resource_id], resource_id)

            if best_key is None or key < best_key:
                best_key = key
                best_resource = resource_id

        assert best_resource is not None
        resource_to_tasks[best_resource].append(task.task_id)
        loads[best_resource] += task.duration

    return resource_to_tasks


def try_move_improvement(
    resource_to_tasks: Dict[str, List[str]],
    task_map: Dict[str, Task],
    compatible_resources: Dict[str, List[str]],
) -> bool:
    """
    Intenta mover una tarea desde el recurso más cargado a otro compatible
    si eso reduce el makespan.
    """
    loads = compute_resource_loads(resource_to_tasks, task_map)
    if not loads:
        return False

    max_resource = max(loads, key=loads.get)
    current_makespan = loads[max_resource]

    # Probar primero tareas grandes del recurso crítico
    candidate_tasks = sorted(
        resource_to_tasks[max_resource],
        key=lambda task_id: (-task_map[task_id].duration, task_id),
    )

    best_move: Optional[Tuple[str, str]] = None
    best_new_makespan = current_makespan

    for task_id in candidate_tasks:
        duration = task_map[task_id].duration

        for target_resource in compatible_resources[task_id]:
            if target_resource == max_resource:
                continue

            new_load_max_resource = loads[max_resource] - duration
            new_load_target = loads[target_resource] + duration

            simulated_max = new_load_target
            for resource_id, load in loads.items():
                if resource_id == max_resource:
                    simulated_max = max(simulated_max, new_load_max_resource)
                elif resource_id == target_resource:
                    simulated_max = max(simulated_max, new_load_target)
                else:
                    simulated_max = max(simulated_max, load)

            if simulated_max < best_new_makespan:
                best_new_makespan = simulated_max
                best_move = (task_id, target_resource)

    if best_move is None:
        return False

    task_id, target_resource = best_move
    resource_to_tasks[max_resource].remove(task_id)
    resource_to_tasks[target_resource].append(task_id)
    return True


def try_swap_improvement(
    resource_to_tasks: Dict[str, List[str]],
    task_map: Dict[str, Task],
    compatible_resources: Dict[str, List[str]],
) -> bool:
    """
    Intenta intercambiar una tarea del recurso más cargado con una tarea de otro recurso.
    """
    loads = compute_resource_loads(resource_to_tasks, task_map)
    if not loads:
        return False

    max_resource = max(loads, key=loads.get)
    current_makespan = loads[max_resource]

    tasks_on_max = sorted(
        resource_to_tasks[max_resource],
        key=lambda task_id: (-task_map[task_id].duration, task_id),
    )

    best_swap: Optional[Tuple[str, str, str]] = None
    best_new_makespan = current_makespan

    for task_a in tasks_on_max:
        dur_a = task_map[task_a].duration

        for other_resource, other_tasks in resource_to_tasks.items():
            if other_resource == max_resource:
                continue

            for task_b in other_tasks:
                dur_b = task_map[task_b].duration

                # Compatibilidad cruzada
                if other_resource not in compatible_resources[task_a]:
                    continue
                if max_resource not in compatible_resources[task_b]:
                    continue

                new_load_max = loads[max_resource] - dur_a + dur_b
                new_load_other = loads[other_resource] - dur_b + dur_a

                simulated_max = 0
                for resource_id, load in loads.items():
                    if resource_id == max_resource:
                        simulated_max = max(simulated_max, new_load_max)
                    elif resource_id == other_resource:
                        simulated_max = max(simulated_max, new_load_other)
                    else:
                        simulated_max = max(simulated_max, load)

                if simulated_max < best_new_makespan:
                    best_new_makespan = simulated_max
                    best_swap = (task_a, task_b, other_resource)

    if best_swap is None:
        return False

    task_a, task_b, other_resource = best_swap

    idx_a = resource_to_tasks[max_resource].index(task_a)
    idx_b = resource_to_tasks[other_resource].index(task_b)

    resource_to_tasks[max_resource][idx_a] = task_b
    resource_to_tasks[other_resource][idx_b] = task_a
    return True


def reorder_within_resources(
    resource_to_tasks: Dict[str, List[str]],
    task_map: Dict[str, Task],
) -> None:
    """
    Reordenamiento interno:
    ordenar por duración descendente dentro de cada recurso.
    Como no hay precedencias ni release times, esto no empeora la validez
    y suele dejar una estructura más estable.
    """
    for resource_id in resource_to_tasks:
        resource_to_tasks[resource_id].sort(
            key=lambda task_id: (-task_map[task_id].duration, task_id)
        )


def improve_solution(
    resource_to_tasks: Dict[str, List[str]],
    task_map: Dict[str, Task],
    compatible_resources: Dict[str, List[str]],
    time_limit_seconds: float,
    start_time: float,
) -> None:
    """
    Búsqueda local liviana:
    - reordenar internamente
    - mover tareas
    - intercambiar tareas
    - cortar por tiempo
    """
    reorder_within_resources(resource_to_tasks, task_map)

    while True:
        if time.perf_counter() - start_time >= time_limit_seconds:
            return

        improved = try_move_improvement(
            resource_to_tasks, task_map, compatible_resources
        )
        if improved:
            reorder_within_resources(resource_to_tasks, task_map)
            continue

        if time.perf_counter() - start_time >= time_limit_seconds:
            return

        improved = try_swap_improvement(
            resource_to_tasks, task_map, compatible_resources
        )
        if improved:
            reorder_within_resources(resource_to_tasks, task_map)
            continue

        break


def main() -> None:
    program_start = time.perf_counter()

    target_makespan: Optional[int] = None
    if len(sys.argv) > 1:
        try:
            target_makespan = int(sys.argv[1])
        except ValueError:
            print("Advertencia: makespan_objetivo inválido. Se ignorará.")

    base_dir = Path(__file__).resolve().parent
    tasks_file = base_dir / "tareas.txt"
    resources_file = base_dir / "recursos.txt"
    output_file = base_dir / "output.txt"

    tasks = read_tasks(tasks_file)
    resources = read_resources(resources_file)

    task_map, resource_map, compatible_resources = build_compatibility(tasks, resources)

    # Construcción inicial
    resource_to_tasks = initial_solution(
        tasks, resources, compatible_resources, resource_map
    )

    # Mejora local con margen amplio respecto al límite de 10s
    improve_solution(
        resource_to_tasks=resource_to_tasks,
        task_map=task_map,
        compatible_resources=compatible_resources,
        time_limit_seconds=8.5,
        start_time=program_start,
    )


    assignments = build_schedule_from_resource_tasks(resource_to_tasks, task_map)

    if not verify_solution(tasks, resources, assignments):
        raise RuntimeError("La solución generada es inválida.")

    write_output(output_file, assignments)

    makespan = compute_makespan(assignments)
    elapsed = time.perf_counter() - program_start

    print(f"Output generado en: {output_file}")
    print(f"Makespan: {makespan}")
    if target_makespan is not None:
        if makespan <= target_makespan:
            print(f"Objetivo cumplido: {makespan} <= {target_makespan}")
        else:
            print(f"Objetivo no cumplido: {makespan} > {target_makespan}")
    print(f"Tiempo de ejecución: {elapsed:.6f} segundos")


if __name__ == "__main__":
    main()



    #Hola! Este código es un programa de asignación de tareas a recursos con el objetivo de minimizar el makespan (el tiempo total para completar todas las tareas). El programa lee tareas y recursos desde archivos CSV, construye una solución inicial basada en heurísticas, y luego mejora esa solución utilizando una búsqueda local. Finalmente, verifica la validez de la solución y escribe los resultados en un archivo de salida.