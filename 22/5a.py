from collections import defaultdict
from dataclasses import dataclass

import rich.console
from aocd.models import Puzzle
from more_itertools import chunked

YEAR = 2022
DAY = 5

c = rich.console.Console()
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(
    f"{puzzle.title} ({YEAR}-{DAY})"
)  # ##########################################################
# print(puzzle.input_data)


def parse_diagram():
    stacks = defaultdict(list)
    for line in puzzle.input_data.splitlines():
        if line.startswith(" 1"):
            break
        for i, chunk in enumerate(chunked(line, 4)):
            if chunk[1] != " ":
                stacks[i + 1].append(chunk[1])
    for key in stacks:
        stacks[key] = stacks[key][::-1]
    return stacks


stacks = parse_diagram()
print(stacks)
print(puzzle.input_data[:500])

lines = puzzle.input_data.splitlines(keepends=False)[10:]

for line in lines:
    tokens = line.split()
    move, from_, to = int(tokens[1]), int(tokens[3]), int(tokens[5])
    for i in range(move):
        stacks[to].append(stacks[from_].pop())

result = ""
for i in range(1, 10):
    result += stacks[i][-1]
print(stacks)
print(result)


c.rule("END")  # ##########################################################
puzzle.answer_a = result
# puzzle.answer_b = overlaps
