from dataclasses import dataclass
from functools import lru_cache
from typing import Tuple, Set, List

YEAR = 2021
DAY = 8

import time

start_time = time.perf_counter()

from aocd import get_data, submit
from rich.console import Console

data = get_data(year=YEAR, day=DAY)
c = Console()
c.rule("START")
# data = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"


@dataclass(frozen=True)
class Entry:
    patterns: List[Set[str]]
    outputs: List[Set[str]]

    def get_unsolved_of_length(self, length, key):
        return [i for i in self.patterns if len(i) == length and i not in key]


entries = []
for line in data.strip().split("\n"):
    left, right = line.strip().split("|")
    patterns = sorted([set(i) for i in left.strip().split()], key=lambda x: len(x))
    outputs = [set(i) for i in right.strip().split()]
    entries.append(Entry(patterns, outputs))
c.print(entries)


def solve_entry(entry: Entry):
    map = {}
    key = [None] * 10
    key[1] = set(entry.patterns[0])
    key[4] = set(entry.patterns[2])
    key[7] = set(entry.patterns[1])
    key[8] = set(entry.patterns[9])
    map["a"] = key[7].difference(key[1]).pop()

    for pattern in entry.get_unsolved_of_length(5, key):
        # these are all the patterns of length 5
        c.print(f"{pattern - key[1]=}")
        if len(pattern - key[1]) == 3:
            key[3] = pattern
    for pattern in entry.get_unsolved_of_length(5, key):
        c.print(f"{pattern - key[4]=}")
        if len(pattern - key[4]) == 2:
            key[5] = pattern
        else:
            key[2] = pattern

    print("stage 3")
    for pattern in entry.get_unsolved_of_length(6, key):
        c.print(f"{pattern - key[1]=}")
        if len(pattern - key[1]) == 5:
            key[6] = pattern
    print("stage 4")
    for pattern in entry.get_unsolved_of_length(6, key):
        c.print(f"{pattern - key[3]=}")
        if len(pattern - key[3]) == 1:
            key[9] = pattern
        else:
            key[0] = pattern

    decoded = int("".join([str(key.index(output)) for output in entry.outputs]))
    c.print(f"{decoded = }")
    return decoded


sum = 0
for entry in entries:
    sum += solve_entry(entry)
answer = sum
c.print(f"{answer = }")

c.rule(f"FINISH {time.perf_counter() - start_time}")

submit(answer, day=DAY, part="b", year=YEAR)
