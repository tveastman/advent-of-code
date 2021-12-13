from collections import defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from itertools import combinations, product, permutations, combinations_with_replacement
from typing import Tuple, Set, List, Dict, DefaultDict, Optional, FrozenSet
import re

from more_itertools import chunked

YEAR = 2021
DAY = 13

import time
from aocd import get_data, submit
from rich.console import Console

start_time = time.perf_counter()
c = Console()
data = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""


data = get_data(year=YEAR, day=DAY)
c.rule("START")


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def fold(self, x: Optional[int] = None, y: Optional[int] = None):
        if y is not None:
            new_y = y - (self.y - y) if self.y > y else self.y
            return Point(self.x, new_y)
        if x is not None:
            new_x = x - (self.x - x) if self.x > x else self.x
            return Point(new_x, self.y)

    @classmethod
    def fold_list(cls, points, x, y):
        return [point.fold(x, y) for point in points]


def parse(data):
    points, instructions = data.strip().split("\n\n")
    points = [
        Point(int(x), int(y))
        for x, y in [line.split(",") for line in points.strip().split("\n")]
    ]
    folds = []
    for line in instructions.strip().split("\n"):
        match = re.search(r"fold along (x|y)=(\d+)", line)
        folds.append((match.group(1), int(match.group(2))))
    return points, folds


points, folds = parse(data)
answer_a = None
for fold in folds:
    if fold[0] == "y":
        points = Point.fold_list(points, x=None, y=fold[1])
    if fold[0] == "x":
        points = Point.fold_list(points, x=fold[1], y=None)
    if answer_a is None:
        answer_a = len(set(points))

points_set = set(points)
c.print(points_set)

max_x = max(p.x for p in points_set)
max_y = max(p.y for p in points_set)
for y in range(max_y + 1):
    for x in range(max_x + 1):
        if Point(x, y) in points_set:
            print("#", end="")
        else:
            print(" ", end="")
    print()
print()


c.rule(f"FINISH {time.perf_counter() - start_time}")

# print(f"{answer = }")
# submit(answer_a, day=DAY, part="a", year=YEAR)
