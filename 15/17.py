import typing

import attrs
import re
import rich.console
from aocd.models import Puzzle

YEAR = 2015
DAY = 17

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")

containers = [int(i) for i in puzzle.input_data.split()]
containers.sort()

TARGET = 150
MIN_CONTAINERS = 4
MAX_CONTAINERS = 11

smallest_set = None
total_solutions = 0
import itertools
for num_containers in range(MIN_CONTAINERS, MAX_CONTAINERS+1):
    solutions = 0
    for combination in itertools.combinations(containers, num_containers):
        if sum(combination) == TARGET:
            solutions += 1
    print(f"{num_containers=}, {solutions=}")
    total_solutions += solutions
    if smallest_set is None:
        smallest_set = solutions

print(f"{total_solutions=}")
puzzle.answer_a = total_solutions
puzzle.answer_b = smallest_set
