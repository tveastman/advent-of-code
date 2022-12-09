from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import PurePath, PurePosixPath

import rich.console
from aocd.models import Puzzle
from more_itertools import chunked
from rich import print

YEAR = 2022
DAY = 9

console = rich.console.Console()
puzzle = Puzzle(year=YEAR, day=DAY)
console.rule(
    f"{puzzle.title} ({YEAR}-{DAY})"
)  # ##########################################################

# data = puzzle.example_data
data = puzzle.input_data
# data = """R 4
# U 4
# L 3
# D 1
# R 4
# D 1
# L 5
# R 2"""
print(data)

H, T = 0j, 0j
U, D, L, R = 1j, -1j, -1, +1

instructions = dict(U=U, D=D, L=L, R=R)
tail_positions = set()
tail_positions.add(T)


def move_tail(h: complex, t: complex, m: complex) -> complex:
    d = h - t
    if abs(d.imag) < 2 and abs(d.real) < 2:
        tail_positions.add(t)
        return t
    t = t + m
    if m.real:
        t = complex(t.real, h.imag)
    elif m.imag:
        t = complex(h.real, t.imag)
    tail_positions.add(t)
    return t


def move_head(h, t, m):
    h += m
    t = move_tail(h, t, m)
    print("move head", h, t)
    return h, t


for line in data.split("\n"):
    i, c = line.split()
    m = instructions[i]
    count = int(c)
    for x in range(count):
        H, T = move_head(H, T, m)

print(tail_positions)
print(len(tail_positions))

console.rule("END")  # ##########################################################
puzzle.answer_a = len(tail_positions)
# puzzle.answer_b = highest_score
