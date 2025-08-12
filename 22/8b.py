from dataclasses import dataclass

import rich.console
from aocd.models import Puzzle
from rich import print

YEAR = 2022
DAY = 8

console = rich.console.Console()
puzzle = Puzzle(year=YEAR, day=DAY)
console.rule(
    f"{puzzle.title} ({YEAR}-{DAY})"
)  # ##########################################################

# data = puzzle.example_data
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


def score(p):
    up, down, left, right = 0, 0, 0, 0
    for y in range(p.y - 1, -1, -1):
        neighbor = points.get(P(p.x, y))
        if neighbor is None:
            break
        up += 1
        if neighbor >= points[p]:
            break
    for y in range(p.y + 1, size):
        neighbor = points.get(P(p.x, y))
        if neighbor is None:
            break
        down += 1
        if neighbor >= points[p]:
            break
    for x in range(p.x - 1, -1, -1):
        neighbor = points.get(P(x, p.y))
        if neighbor is None:
            break
        left += 1
        if neighbor >= points[p]:
            break
    for x in range(p.x + 1, size):
        neighbor = points.get(P(x, p.y))
        if neighbor is None:
            break
        right += 1
        if neighbor >= points[p]:
            break
    return up * down * left * right


highest_score = max(score(p) for p in points)
print(highest_score)

console.rule("END")  # ##########################################################
# puzzle.answer_a = len(visible_trees)
puzzle.answer_b = highest_score
