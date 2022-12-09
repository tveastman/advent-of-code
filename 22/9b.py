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
# data = """R 5
# U 8
# L 8
# D 3
# R 17
# D 10
# L 25
# U 20"""
print(data)

rope = [0j] * 10
U, D, L, R = 1j, -1j, -1, +1

instructions = dict(U=U, D=D, L=L, R=R)
tail_positions = set()


def move_tail(h: complex, t: complex) -> complex:
    d = h - t
    if abs(d.real) < 2 and abs(d.imag) < 2:
        return t
    if d == U + U:
        return t + U
    elif d == D + D:
        return t + D
    elif d == L + L:
        return t + L
    elif d == R + R:
        return t + R
    elif d.real > 0 and d.imag > 0:
        return t + R + U
    elif d.real > 0 and 0 > d.imag:
        return t + R + D
    elif 0 > d.real and d.imag > 0:
        return t + L + U
    elif 0 > d.real and 0 > d.imag:
        return t + L + D


def move_rope(rope, m):
    rope[0] += m
    for i in range(1, len(rope)):
        t = move_tail(rope[i - 1], rope[i])
        rope[i] = t
    tail_positions.add(rope[-1])


for line in data.split("\n"):
    i, c = line.split()
    m = instructions[i]
    count = int(c)
    for x in range(count):
        move_rope(rope, m)
        tail_positions.add(rope[-1])
        # print(f"{rope=}")

print(rope)
print(tail_positions)
print(len(tail_positions))

console.rule("END")  # ##########################################################
# puzzle.answer_a = len(tail_positions)
puzzle.answer_b = len(tail_positions)
