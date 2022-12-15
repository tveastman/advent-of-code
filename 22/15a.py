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

TARGET_ROW = 2_000_000
s = set()
for sensor, md in sensors.items():
    x1, x2 = sensor.y_coverage(TARGET_ROW, md)
    if x1 is None:
        continue
    print(f"processing {sensor=}, {md=}")
    s.update(i for i in range(x1, x2 + 1))
for beacon in known_beacons:
    if beacon.y == TARGET_ROW:
        s.discard(beacon.x)
# print(sorted(s))
print(len(s))
puzzle.answer_a = len(s)
console.rule("END")  # ##########################################################
