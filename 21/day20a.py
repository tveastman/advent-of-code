from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Dict

YEAR = 2021
DAY = 20

import time
from aocd import get_data, submit
from rich.console import Console

start_time = time.perf_counter()
c = Console()
print = c.print

data = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""
data = get_data(year=YEAR, day=DAY)

c.rule("START")
# c.print(data)


@dataclass(frozen=True)
class P:
    x: int
    y: int

    def neighbourhood(self):
        return tuple(
            P(self.x + dx, self.y + dy)
            for dx, dy in sorted(
                product(range(-1, 2), range(-1, 2)), key=lambda x: (x[1], x[0])
            )
        )


GridType = Dict[P, str]


def grid_value(grid: GridType, p: P, default_border) -> int:
    s = []
    for n in p.neighbourhood():
        v = grid.get(n, default_border)
        v = "1" if v == "#" else "0"
        s.append(v)
    result = int("".join(s), 2)
    # print(p, result)
    return result


def parse(data: str) -> tuple[str, GridType]:
    lines = data.strip().split("\n")
    algorithm = lines[0]

    grid = {}
    for y, line in enumerate(lines[2:]):
        for x, char in enumerate(line):
            grid[P(x, y)] = char
    return algorithm, grid


def ENHANCE_exclamation_point(algorithm, grid, default_border):
    min_x, max_x, min_y, max_y = 0, 0, 0, 0
    for p in grid.keys():
        x, y = p.x, p.y
        min_x = x if x < min_x else min_x
        max_x = x if x > max_x else max_x
        min_y = y if y < min_y else min_y
        max_y = y if y > max_y else max_y

    enhanced: GridType = dict()
    print("bounds:", min_x, max_x, min_y, max_y)
    for x in range(min_x - 2, max_x + 3):
        for y in range(min_y - 2, max_y + 3):
            p = P(x, y)
            gv = grid_value(grid, p, default_border=default_border)
            decoded_char = algorithm[gv]
            enhanced[p] = decoded_char
    return enhanced


algorithm, grid = parse(data)

# print(grid)
# gv = grid_value(grid, P(2, 2))
# print(gv)
grid = ENHANCE_exclamation_point(algorithm, grid, ".")
grid = ENHANCE_exclamation_point(algorithm, grid, "#")
# enhanced = ENHANCE_exclamation_point(algorithm, enhanced)
# print(f"{len(enhanced) = }")
# print(enhanced)

lit_pixels = sum(1 for i in grid.values() if i == "#")
print(f"{lit_pixels = }")
submit(lit_pixels, year=YEAR, day=DAY, part="a")
for i in range(24):
    grid = ENHANCE_exclamation_point(algorithm, grid, ".")
    grid = ENHANCE_exclamation_point(algorithm, grid, "#")

lit_pixels = sum(1 for i in grid.values() if i == "#")
print(f"{lit_pixels = }")
submit(lit_pixels, year=YEAR, day=DAY, part="b")


c.rule(f"FINISH {time.perf_counter() - start_time}")
