import modulefinder
import operator
import re
import signal
import string
import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import reduce
from pathlib import PurePath, PurePosixPath
from typing import List, Dict, Optional

import networkx
import rich.console
import sortedcontainers
from aocd.models import Puzzle
from intervaltree import IntervalTree, Interval
from more_itertools import chunked
from networkx import shortest_path
from rich import print
from sortedcontainers import SortedSet

YEAR = 2022
DAY = 15

console = rich.console.Console()
puzzle = Puzzle(year=YEAR, day=DAY)
console.rule(
    f"{puzzle.title} ({YEAR}-{DAY})"
)  # ##########################################################
data = puzzle.input_data
# data = puzzle.example_data
print("[bold]data\n", data)


@dataclass(frozen=True, order=True)
class P:
    x: int
    y: int

    def __add__(self, other):
        return P(self.x + other.x, self.y + other.y)

    def md(self, other) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def y_coverage(self, y, md):
        "Returns the x co-ords reachable on that y axis if you can move md from self"
        distance = abs(self.y - y)
        remainder = md - distance
        if remainder < 0:
            return None, None
        x1 = self.x - remainder
        x2 = self.x + remainder
        return x1, x2

    @property
    def freq(self):
        return (self.x * 4_000_000) + self.y


# Each sensors and their "no-beacon-in-this-range
sensors: Dict[P, int] = {}
known_beacons = set()
for line in data.splitlines():
    m = [int(i) for i in re.findall(r"-?\d+", line)]
    sensor, nearest_beacon = P(m[0], m[1]), P(m[2], m[3])
    md = sensor.md(nearest_beacon)
    known_beacons.add(nearest_beacon)
    sensors[sensor] = md
print(sensors)
print(known_beacons)

X_SEARCH_START = 0
X_SEARCH_FINISH = 4_000_000
# X_SEARCH_FINISH = 20

Y_SEARCH_START = 0
Y_SEARCH_FINISH = 4_000_000
# Y_SEARCH_FINISH = 20

for y in range(Y_SEARCH_START, Y_SEARCH_FINISH + 1):
    t = IntervalTree([Interval(X_SEARCH_START, X_SEARCH_FINISH + 1)])
    for sensor, md in sensors.items():
        x1, x2 = sensor.y_coverage(y, md)
        if x1 is None:
            continue
        t.chop(x1, x2 + 1)
    if t:
        print(f"finished? {y=}, {t=}")
        break
    if y % 10000 == 0:
        print("up to ", y)

x = t.all_intervals.pop().begin
y = y
result = P(x, y)
print(f"{result=}, {result.freq=}")
puzzle.answer_b = result.freq

console.rule("END")  # ##########################################################
