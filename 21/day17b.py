from __future__ import annotations

import typing
from dataclasses import dataclass, field
from functools import lru_cache
from typing import List, Dict, Optional
from enum import Enum, auto
from io import StringIO

YEAR = 2021
DAY = 17

import time
from aocd import get_data, submit
from rich.console import Console

start_time = time.perf_counter()
c = Console()

data = get_data(year=YEAR, day=DAY)
c.rule("START")


class Result(Enum):
    PENDING = auto()
    HIT = auto()
    MISS = auto()


@dataclass(frozen=True)
class Vector:
    x: int
    y: int


@dataclass(frozen=True)
class Area:
    xmin: int
    xmax: int
    ymin: int
    ymax: int

    def hit_y(self, probe):
        if self.ymin <= probe.p.y and probe.p.y <= self.ymax:
            return Result.HIT
        if probe.p.y < self.ymin and probe.v.y < 0:
            return Result.MISS
        else:
            return Result.PENDING

    def hit_x(self, probe):
        if self.xmin <= probe.p.x and probe.p.x <= self.xmax:
            return Result.HIT
        elif probe.v.x == 0 and probe.p.x < self.xmin:
            return Result.MISS
        elif probe.p.x > self.xmax:
            return Result.MISS
        else:
            return Result.PENDING

    def hit(self, probe):
        x, y = self.hit_x(probe), self.hit_y(probe)
        if x is Result.HIT and y is Result.HIT:
            return Result.HIT
        elif x is Result.MISS or y is Result.MISS:
            return Result.MISS
        else:
            return Result.PENDING


@dataclass(frozen=True)
class Probe:
    p: Vector
    v: Vector

    @lru_cache(maxsize=0)
    def step(self):
        dvx = 0 if self.v.x == 0 else -1 if self.v.x > 0 else 1
        return Probe(
            p=Vector(x=self.p.x + self.v.x, y=self.p.y + self.v.y),
            v=Vector(x=self.v.x + dvx, y=self.v.y - 1),
        )

    def shoot(self, area):
        probe = self
        while True:
            h = area.hit(probe)
            if h is not Result.PENDING:
                return h
            probe = probe.step()


origin = Vector(0, 0)
target = Area(155, 215, -132, -72)

x_search_space = range(17, 216)
y_search_space = range(-133, 133)

hits = set()
for x in x_search_space:
    for y in y_search_space:
        initial_velocity = Vector(x, y)
        # c.print(initial_velocity)
        probe = Probe(p=origin, v=initial_velocity)
        result = probe.shoot(target)
        if result is Result.HIT:
            hits.add(initial_velocity)
    print(f"{len(hits) = } , {x = }")

c.print(hits)
c.print(len(hits))
c.print(data)
probe = Probe(p=origin, v=Vector(180, -100))
c.print(probe.shoot(target))
c.rule(f"FINISH {time.perf_counter() - start_time}")
