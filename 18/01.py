import rich.console
from aocd import puzzle
from aocd.models import Puzzle


YEAR = 2018
DAY = 1

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")

one_line = puzzle.input_data.replace("\n", " ")
puzzle.answer_a = eval(one_line)

instructions = [int(i) for i in puzzle.input_data.split()]
print(instructions)
f = 0
seen = {f}
counter = 0
while True:
    for i in instructions:
        counter += 1
        f += i
        if f in seen:
            print(f"{counter=}: we've seen {f=}")
            puzzle.answer_b = f
            import sys

            sys.exit(0)
        else:
            seen.add(f)
print(f"Repeating list, {len(seen)=}")
