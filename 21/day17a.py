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
        ymax = self.p.y
        probe = self
        while True:
            if probe.p.y < area.ymin and probe.v.y < 0:
                return Result.MISS, ymax
            elif area.ymin <= probe.p.y and probe.p.y <= area.ymax:
                print(ymax)
                return Result.HIT, ymax
            probe = probe.step()
            ymax = max(ymax, probe.p.y)


origin = Vector(0, 0)
target = Area(
    # 155, 215,
    0,
    0,
    -132,
    -72,
)

hit_ymax = None
for vy in range(500, 0, -1):
    p = Probe(origin, v=Vector(0, vy))
    r, ymax = p.shoot(target)

c.print(data)
c.rule(f"FINISH {time.perf_counter() - start_time}")
