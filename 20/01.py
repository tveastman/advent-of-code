import rich.console
from aocd.models import Puzzle
from functools import reduce
from operator import mul
from itertools import combinations

YEAR = 2020
DAY = 1

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")

expenses = list(int(i) for i in puzzle.input_data.split())
print(expenses)
for a, b in combinations(expenses, 2):
    if a + b == 2020:
        break
puzzle.answer_a = a * b


for seq in combinations(expenses, 3):
    if sum(seq) == 2020:
        break
puzzle.answer_b = reduce(mul, seq)
c.rule()
