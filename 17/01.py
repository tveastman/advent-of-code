import rich.console
from aocd.models import Puzzle

YEAR = 2017
DAY = 1

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")

input = list(puzzle.input_data)
digits = list(input)
digits.append(digits[0])

s = 0
for i in range(1, len(digits)):
    if digits[i - 1] == digits[i]:
        s += int(digits[i])
puzzle.answer_a = s

c.rule()

input = puzzle.input_data
digits = list(input)

s = 0
for i in range(len(digits)):
    j = (i + (len(digits) // 2)) % len(digits)
    if digits[i] == digits[j]:
        s += int(digits[i])
print(s)
puzzle.answer_b = s
