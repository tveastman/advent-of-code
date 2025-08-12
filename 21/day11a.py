from dataclasses import dataclass, field
from itertools import product
from typing import List, Dict


YEAR = 2021
DAY = 11

import time
from aocd import get_data, submit
from rich.console import Console

start_time = time.perf_counter()
c = Console()
data = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""
data = get_data(year=YEAR, day=DAY)
c.rule("START")


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass()
class Octopus:
    point: Point
    energy: int


@dataclass()
class Grid:
    h: int
    w: int
    d: Dict[Point, Octopus] = field(default_factory=dict)
    s: int = 0  # step
    f: int = 0  # total flashes

    def neighbours(self, p: Point) -> List[Octopus]:
        ns: List[Octopus] = []
        for dx, dy in product(range(-1, 2), range(-1, 2)):
            if not dx and not dy:
                continue
            o = self.d.get(Point(x=p.x + dx, y=p.y + dy))
            if o:
                ns.append(o)
        return ns

    def print(self):
        c.print(f"Step {self.s}, total flashes {self.f}")
        for y in range(self.h):
            line = []
            for x in range(self.w):
                o = self.d[Point(x, y)]
                if o.energy == 0:
                    line.append("[bold yellow]0[/]")
                else:
                    line.append(str(o.energy))
            c.print(" ".join(line))

    def step(self):
        self.s += 1
        flash: List[Octopus] = list()
        for k, v in self.d.items():
            v.energy += 1
            if v.energy > 9:
                flash.append(v)
        self.flash(flash)

    def flash(self, octopi: List[Octopus]):
        while len(octopi):
            o = octopi.pop()
            if o.energy == 0:
                continue
            o.energy = 0
            self.f += 1
            for n in self.neighbours(o.point):
                if n.energy == 0:
                    continue
                n.energy += 1
                if n.energy > 9:
                    octopi.append(n)


grid = Grid(h=10, w=10)
for y, line in enumerate(data.strip().split("\n")):
    for x, chr in enumerate(line.strip()):
        grid.d[Point(x, y)] = Octopus(Point(x, y), int(chr))

grid.print()

answer_a = None
prev_f = 0
while True:
    grid.step()
    grid.print()
    c.print()

    if grid.s == 100:
        answer_a = grid.f

    if grid.f - prev_f == grid.w * grid.h:
        answer_b = grid.s
        break
    prev_f = grid.f

c.rule(f"FINISH {time.perf_counter() - start_time}")
submit(answer_a, day=DAY, part="a", year=YEAR)
submit(answer_b, day=DAY, part="b", year=YEAR)
