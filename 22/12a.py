import modulefinder
import operator
import string
import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import reduce
from pathlib import PurePath, PurePosixPath
from typing import List, Dict

import networkx
import rich.console
from aocd.models import Puzzle
from more_itertools import chunked
from networkx import shortest_path
from rich import print

YEAR = 2022
DAY = 12

console = rich.console.Console()
puzzle = Puzzle(year=YEAR, day=DAY)
console.rule(
    f"{puzzle.title} ({YEAR}-{DAY})"
)  # ##########################################################
data = puzzle.input_data
# data = puzzle.example_data
print(data)

elevations = "S" + string.ascii_lowercase + "E"
scores = {char: i for i, char in enumerate(elevations)}
print(scores)


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point"):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point"):
        return Point(self.x - other.x, self.y - other.y)


UP, DOWN, LEFT, RIGHT = Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0)


@dataclass(frozen=True)
class Square:
    p: Point
    e: int


def neighbours(squares, square):
    result = set()
    for direction in [UP, DOWN, LEFT, RIGHT]:
        n = squares.get(square.p + direction)
        if n is not None:
            if n.e <= square.e + 1:
                result.add(n)
    return result


start: Square
end: Square

squares: Dict[Point, Square] = {}
for y, line in enumerate(data.splitlines()):
    for x, char in enumerate(line):
        p = Point(x, y)
        s = Square(p, scores[char])
        if char == "S":
            start = s
        if char == "E":
            end = s
        squares[p] = s

graph = networkx.DiGraph()
for p, square in squares.items():
    graph.add_node(square)
for p, square in squares.items():
    for n in neighbours(squares, square):
        graph.add_edge(square, n)

print(graph)
print(neighbours(squares, start))

sp = shortest_path(graph, start, end)
steps = len(sp) - 1
print(f"{steps=}")
puzzle.answer_a = steps


for p, square in squares.items():
    if square.e != 1:
        continue
    try:
        path = shortest_path(graph, square, end)
        path_steps = len(path) - 1
        steps = steps if steps < path_steps else path_steps
    except:
        pass

print(f"{steps=}")
puzzle.answer_b = steps

console.rule("END")  # ##########################################################
