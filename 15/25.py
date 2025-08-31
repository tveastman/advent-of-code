import typing

import attrs
import re
import rich.console
from aocd.models import Puzzle

YEAR = 2015
DAY = 25

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")

row, column = (int(i) for i in re.search(r"(\d+)[^\d]+(\d+)", puzzle.input_data).groups())

def get_code(num: int = 1) -> int:
    v = 20151125
    for i in range(num-1):
        v = v * 252_533 % 33_554_393
    return v

def sequence_for(row: int, column: int) -> int:
    result = 1
    increment = 1
    for i in range(row-1):
        result += increment
        increment += 1
    increment = 1
    for i in range(column-1):
        result += row + increment
        increment += 1
    return result

print(f"{row=}, {column=} {sequence_for(row, column)=}")
target = sequence_for(row, column)

puzzle_code = get_code(sequence_for(row, column))
puzzle.answer_a = puzzle_code

