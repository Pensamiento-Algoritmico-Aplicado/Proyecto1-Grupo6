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