from collections import defaultdict, deque
from dataclasses import dataclass

import rich.console
from aocd.models import Puzzle
from more_itertools import chunked

YEAR = 2022
DAY = 6

c = rich.console.Console()
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(
    f"{puzzle.title} ({YEAR}-{DAY})"
)  # ##########################################################
print(puzzle.example_data)

sequence_length = 14
d = deque(maxlen=sequence_length)
for i, char in enumerate(puzzle.input_data):
    d.append(char)
    if len(d) == sequence_length:
        s = set(d)
        print(s)
        if len(s) == sequence_length:
            break

print(i + 1)

c.rule("END")  # ##########################################################
# puzzle.answer_a = i+1
puzzle.answer_b = i + 1
