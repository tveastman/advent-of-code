import typing

import attrs
import re
import rich.console
from aocd.models import Puzzle
import array
import itertools

YEAR = 2015
DAY = 20

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")


def factors(n):
    result = set()
    for i in range(1, int(n**0.5) + 1):
        div, mod = divmod(n, i)
        if mod == 0:
            result |= {i, div}
    return result


def gifts_at_house(n):
    return sum(10 * factor for factor in factors(n))


target = int(puzzle.input_data)
import math

# num_houses = math.factorial(10)
num_houses = 1_000_000
houses = array.array("L", [0] * (num_houses + 1))
print(f"{target=}")
finished = False
for elf in range(1, len(houses)):
    for i in range(elf, len(houses), elf):
        houses[i] += 10 * elf

print("searching")
for i in range(len(houses)):
    if houses[i] >= target:
        print(f"{i=}, {houses[i]=}")
        break
puzzle.answer_a = i


num_houses = 29_000_000
houses = array.array("L", [0] * (num_houses + 1))
finished = False
for elf in range(1, len(houses)):
    c = 0
    for i in range(elf, len(houses), elf):
        c += 1
        houses[i] += 11 * elf
        if c == 50:
            break

print("searching")
for i in range(len(houses)):
    if houses[i] >= target:
        print(f"{i=}, {houses[i]=}")
        break
puzzle.answer_b = i
