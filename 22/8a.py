from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import PurePath, PurePosixPath

import rich.console
from aocd.models import Puzzle
from more_itertools import chunked
from rich import print

YEAR = 2022
DAY = 8

console = rich.console.Console()
puzzle = Puzzle(year=YEAR, day=DAY)
console.rule(
    f"{puzzle.title} ({YEAR}-{DAY})"
)  # ##########################################################

data = puzzle.example_data
data = puzzle.input_data
size = len(data.splitlines())

print(data)


@dataclass(frozen=True)
class P:
    x: int
    y: int


points = dict()
for l, line in enumerate(data.splitlines()):
    for c, char in enumerate(line):
        points[P(c, l)] = int(char)

visible_trees = set()


def visible(row):
    max = -1
    for p in row:
        height = points[p]
        if height > max:
            visible_trees.add(p)
            max = height


rows = []
for x in range(size):
    row = []
    for y in range(size):
        row.append(P(x, y))
    rows.append(row)
for y in range(size):
    row = []
    for x in range(size):
        row.append(P(x, y))
    rows.append(row)

for row in rows:
    visible(row)
    visible(reversed(row))

print(visible_trees)
print(len(visible_trees))
for y in range(size):
    for x in range(size):
        p = P(x, y)
        if p in visible_trees:
            print(f"[bold][yellow]{points[p]} [/][/]", end="")
        else:
            print(f"[black]{points[p]} [/]", end="")
    print()


print(len(visible_trees))
console.rule("END")  # ##########################################################
puzzle.answer_a = len(visible_trees)
# puzzle.answer_b = cumulative_sizes[candidate]
