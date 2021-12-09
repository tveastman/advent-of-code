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
class Point:
    x: int
    y: int
    z: int


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
        # return self.map[y][x]
        return Point(x, y, self.map[y][x])

    def neighbours(self, x, y):
        n = []
        # for dx, dy in product(range(-1, 2), range(-1, 2)):
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


def find_basin(basins, point):
    """Find the basin this point is in, or return a new basin. Mutates basins."""
    for basin in basins:
        if point in basin:
            return basin
    basin = set()
    basin.add(point)
    basins.append(basin)
    return basin


def search_basin(hm, basin, point):
    ns = [p for p in hm.neighbours(point.x, point.y) if p.z != 9]
    for n in ns:
        if n not in basin:
            basin.add(n)
            search_basin(hm, basin, n)


basins: List[Set[Point]] = list()
for y in range(hm.height):
    for x in range(hm.width):
        p = hm.get(x, y, 0, 0)
        if p.z == 9:
            continue
        b = find_basin(basins, p)
        search_basin(hm, b, p)

basins.sort(key=lambda x: -len(x))
product = 1
for b in basins[:3]:
    product *= len(b)
print(f"{product = }")
answer = product
c.rule(f"FINISH {time.perf_counter() - start_time}")

submit(answer, day=DAY, part="b", year=YEAR)
