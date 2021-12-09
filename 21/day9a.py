from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations, product, permutations, combinations_with_replacement
from typing import Tuple, Set, List

YEAR = 2021
DAY = 9

import time

start_time = time.perf_counter()

from aocd import get_data, submit
from rich.console import Console

data = get_data(year=YEAR, day=DAY)
# data = """2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678
# """
c = Console()
c.rule("START")


@dataclass(frozen=True)
class HeightMap:
    map: Tuple[Tuple[int]]
    width: int
    height: int

    def get(self, x, y, dx, dy):
        x += dx
        y += dy
        if x < 0 or x > self.width - 1:
            return None
        if y < 0 or y > self.height - 1:
            return None
        return self.map[y][x]

    def neighbours(self, x, y):
        n = []
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            if dx == 0 and dy == 0:
                continue
            n.append(self.get(x, y, dx, dy))
        return tuple(i for i in n if i is not None)


def read(data):
    map = []
    for l in data.strip().split("\n"):
        map.append(tuple(int(i) for i in l.strip()))
    return HeightMap(map=tuple(map), width=len(map[0]), height=len(map))


hm = read(data)

risk_level = 0
for x in range(hm.width):
    for y in range(hm.height):
        value = hm.get(x, y, 0, 0)
        ns = hm.neighbours(x, y)
        if all([value < n for n in ns]):
            risk_level += 1 + value

print(f"{risk_level = }")
answer = risk_level
c.rule(f"FINISH {time.perf_counter() - start_time}")

submit(answer, day=DAY, part="a", year=YEAR)
