from __future__ import annotations
import csv
import heapq
import time
from pathlib import Path

def read_tasks(path):
    with open(path, newline="", encoding="utf-8") as f:
        return [(r[0], int(r[1]), r[2]) for r in csv.reader(f) if r]

def read_resources(path):
    with open(path, newline="", encoding="utf-8") as f:
        return [(r[0], tuple(r[1:])) for r in csv.reader(f) if r]
    
def build_compat(tasks, resources):
    cat_map = {}
    r_cats = {}
    for r, cats in resources:
        r_cats[r] = cats
        for c in cats:
            cat_map.setdefault(c, []).append(r)
    compat = {t: cat_map[c] for t, _, c in tasks}
    return compat, r_cats, cat_map

def greedy(tasks, resources, compat, r_cats, cat_map):
    r_to_t = {r: [] for r, _ in resources}
    loads = {r: 0 for r, _ in resources}
    task_map = {t: d for t, d, _ in tasks}

    # Un heap por categoría: (carga_actual, recurso)
    heaps = {}
    for c, rs in cat_map.items():
        h = [(0, r) for r in rs]
        heapq.heapify(h)
        heaps[c] = h

    # Ordenar una vez: largas primero
    tasks_sorted = sorted(tasks, key=lambda x: -x[1])

    for t, d, c in tasks_sorted:
        h = heaps[c]

        # Lazy deletion: si la carga del heap está vieja, la descartamos
        while True:
            load, r = heapq.heappop(h)
            if load == loads[r]:
                break

        r_to_t[r].append(t)
        loads[r] += d

        new_state = (loads[r], r)
        for rc in r_cats[r]:
            heapq.heappush(heaps[rc], new_state)

    return r_to_t, loads, task_map
def improve_once(r_to_t, loads, task_map, compat):
    max_r = max(loads, key=loads.get)
    max_load = loads[max_r]

    if not r_to_t[max_r]:
        return False

    # Probar primero tareas más grandes del recurso crítico
    indexed = sorted(
        enumerate(r_to_t[max_r]),
        key=lambda p: -task_map[p[1]]
    )

    for idx, t in indexed:
        d = task_map[t]

        best_r = None
        best_load = max_load

        for r in compat[t]:
            if r == max_r:
                continue
            if loads[r] < best_load:
                best_load = loads[r]
                best_r = r

        if best_r is not None and loads[best_r] + d < max_load:
            r_to_t[max_r].pop(idx)
            r_to_t[best_r].append(t)
            loads[max_r] -= d
            loads[best_r] += d
            return True

    return False