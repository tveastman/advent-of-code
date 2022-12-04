import rich.console
from aocd.models import Puzzle

YEAR = 2015
DAY = 1

c = rich.console.Console()
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule()  # ##########################################################

floor = 0
basement_step = None
for step, paren in enumerate(puzzle.input_data):
    if paren == "(":
        floor += 1
    elif paren == ")":
        floor -= 1
    if basement_step is None and floor == -1:
        basement_step = step + 1

print(f"{floor=}")
print(f"{basement_step=}")
c.rule()  # ##########################################################
puzzle.answer_a = floor
puzzle.answer_b = basement_step
