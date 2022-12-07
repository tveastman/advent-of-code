from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import PurePath, PurePosixPath

import rich.console
from aocd.models import Puzzle
from more_itertools import chunked
from rich import print

YEAR = 2022
DAY = 7

c = rich.console.Console()
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(
    f"{puzzle.title} ({YEAR}-{DAY})"
)  # ##########################################################
dir_sizes = defaultdict(int)
file_sizes = defaultdict(int)
cwd = PurePosixPath("/")
root = PurePosixPath("/")

print(puzzle.input_data.splitlines()[:30])

for i, line in enumerate(puzzle.input_data.splitlines()):
    print(line)
    tokens = line.strip().split()
    if tokens[:2] == ["$", "cd"]:
        arg = tokens[2]
        if arg == "..":
            cwd = cwd.parent
        else:
            cwd = cwd / arg
    try:
        size, filename = int(tokens[0]), tokens[1]
        file_sizes[cwd / filename] = size
        dir_sizes[cwd] += size
    except:
        pass

cumulative_sizes = defaultdict(int)
for key, value in dir_sizes.items():
    cwd = key
    cumulative_sizes[cwd] += value
    while True:
        if cwd == root:
            break
        cwd = cwd.parent
        cumulative_sizes[cwd] += value

filesystem = 70_000_000
used = cumulative_sizes[root]
unused = filesystem - used
required = 30_000_000

criterion = required - unused
print(f"{criterion=}")


s = 0
candidate = None
for key, value in cumulative_sizes.items():
    if value <= 100_000:
        s += value
    if value >= criterion:
        if candidate is None:
            candidate = key
        if value < cumulative_sizes[candidate]:
            candidate = key


print(s)
print(candidate, cumulative_sizes[candidate])

c.rule("END")  # ##########################################################
puzzle.answer_a = s
puzzle.answer_b = cumulative_sizes[candidate]
