import typing
from functools import cache

import attrs
import rich.console
from aocd.models import Puzzle

YEAR = 2015
DAY = 11

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")


import string

alphabet = list(string.ascii_lowercase)
alphabet.remove("i")
alphabet.remove("o")
alphabet.remove("l")
print(f"{alphabet=}")


@cache
def index_of(chr) -> int:
    return alphabet.index(chr)


def increment(pw, index=-1) -> None:
    current = pw[index]
    new_index = index_of(current) + 1
    if new_index == len(alphabet):
        new_index = 0
        increment(pw, index - 1)
    pw[index] = alphabet[new_index]


def straight(pw):
    for i in range(0, len(pw) - 2):
        a, b, c = pw[i], pw[i + 1], pw[i + 2]
        if ord(c) - ord(b) == 1 and ord(b) - ord(a) == 1:
            return True
    return False


def two_pairs(pw):
    i = 0
    pairs = []
    while i < len(pw) - 1:
        a, b = pw[i], pw[i + 1]
        if a == b and a not in pairs:
            i += 1
            pairs.append(a)
            if len(pairs) == 2:
                return True
        i += 1
    return False


pw = list(puzzle.input_data)
counter = 0

while True:
    counter += 1
    increment(pw)
    if straight(pw) and two_pairs(pw):
        break

password = "".join(pw)
print(f"{counter=}, {password=}")
puzzle.answer_a = password

while True:
    counter += 1
    increment(pw)
    if straight(pw) and two_pairs(pw):
        break

password = "".join(pw)
print(f"{counter=}, {password=}")
puzzle.answer_b = password
