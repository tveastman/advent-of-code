import humanize
import rich.console
from aocd.models import Puzzle
from collections import defaultdict
import networkx as nx
import pyparsing as pp
import itertools

YEAR = 2024
DAY = 1

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")

left, right = [], []
for line in puzzle.input_data.splitlines():
    a, b = line.split()
    left.append(int(a))
    right.append(int(b))

total_distance = 0
for l, r in zip(sorted(left), sorted(right)):
    total_distance += abs(l - r)

print(total_distance)
puzzle.answer_a = total_distance

similarity_score = 0
for l in left:
    count = right.count(l)
    similarity_score += count * l

print(f"{similarity_score=}")
puzzle.answer_b = similarity_score
