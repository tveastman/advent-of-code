import rich.console
from aocd.models import Puzzle

YEAR = 2015
DAY = 2

c = rich.console.Console()
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(
    f"{puzzle.title} ({YEAR}-{DAY})"
)  # ##########################################################

total_paper = 0
total_ribbon = 0
for line in puzzle.input_data.splitlines():
    l, w, h = [int(i) for i in line.split("x")]
    paper = 2 * l * w + 2 * w * h + 2 * h * l + min([l * w, w * h, h * l])
    shortest, shorter = sorted([l, w, h])[:2]
    total_ribbon += shortest + shortest + shorter + shorter + (l * w * h)
    total_paper += paper

print(total_paper)
print(total_ribbon)
c.rule()  # ##########################################################
puzzle.answer_a = total_paper
puzzle.answer_b = total_ribbon
