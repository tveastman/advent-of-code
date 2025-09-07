import typing

import attrs
import re
import rich.console
from aocd.models import Puzzle

YEAR = 2015
DAY = 12

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")

import json

document = json.loads(puzzle.input_data)
print(document)


def dfs(document) -> int:
    if isinstance(document, int):
        return document
    elif isinstance(document, list):
        return sum(dfs(item) for item in document)
    elif isinstance(document, dict):
        return sum(dfs(value) for value in document.values())
    return 0


result = dfs(document)
print(f"{result=}")
puzzle.answer_a = result


def dfs(document) -> int:
    if isinstance(document, int):
        return document
    elif isinstance(document, list):
        return sum(dfs(item) for item in document)
    elif isinstance(document, dict):
        if "red" in document.values():
            return 0
        return sum(dfs(value) for value in document.values())
    return 0


result = dfs(document)
print(f"{result=}")
puzzle.answer_b = result
