from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from functools import cached_property, singledispatch, singledispatchmethod
from itertools import product
from typing import Dict, Tuple, Union, List, Optional
import re

YEAR = 2021
DAY = 22

import time
from aocd import get_data, submit
from rich.console import Console

start_time = time.perf_counter()
c = Console()
print = c.print

data = get_data(year=YEAR, day=DAY)
#print(data)
c.rule("START")


class Switch(Enum):
    on = "on"
    off = "off"


@dataclass(frozen=True)
class P:
    x: int
    y: int
    z: int



@dataclass(frozen=True)
class C:
    min: P
    max: P

    def all_points(self):
        xrange = range(self.min.x, self.max.x + 1)
        yrange = range(self.min.y, self.max.y + 1)
        zrange = range(self.min.z, self.max.z + 1)

        for x in xrange:
            for y in yrange:
                for z in zrange:
                    yield P(x, y, z)

    @cached_property
    def dimensions(self) -> Tuple[int, int, int]:
        x = 1 + self.max.x - self.min.x
        y = 1 + self.max.y - self.min.y
        z = 1 + self.max.z - self.min.z
        return x, y, z

    @cached_property
    def volume(self) -> int:
        x, y, z = self.dimensions
        return x * y * z

    @singledispatchmethod
    def __contains__(self, other):
        return NotImplemented

    @__contains__.register
    def _(self, other: P) -> bool:
        result = (
           self.min.x <= other.x <= self.max.x and
           self.min.y <= other.y <= self.max.y and
           self.min.z <= other.z <= self.max.z
        )
        return result

# TIL you have to register a dispatch for the class *after*
# the class has been created, so this has to sit outside
# the class definition so that 'C' is recognized. Makes
# the implementation ugly.
@C.__contains__.register
def _(self, other: C) -> bool:
    return other.min in self and other.max in self

InstructionsType = List[Tuple[Switch, C]]

def parse(data) -> InstructionsType:
    instructions = []
    for line in data.strip().split('\n'):
        i, line = line.split()
        instruction = Switch(i)
        x, y, z  = line.split(",")
        xmin, xmax = x.split("=")[1].split("..")
        ymin, ymax = y.split("=")[1].split("..")
        zmin, zmax = z.split("=")[1].split("..")
        pmin = P(int(xmin), int(ymin), int(zmin))
        pmax = P(int(xmax), int(ymax), int(zmax))
        instructions.append((instruction, C(pmin, pmax)))
    return instructions

instructions = parse(data)

# def part_a_instructions(instructions: InstructionsType):
#     point_space = set()
#     boundary = C(P(-50, -50, -50), P(50, 50, 50))
#     for switch, cube in instructions:
#         if cube not in boundary:
#             continue
#         if switch is Switch.on:
#             for p in cube.all_points():
#                 point_space.add(p)
#         elif switch is Switch.off:
#             for p in cube.all_points():
#                 point_space.discard(p)
#         print(switch, cube)
#     print(f"{len(point_space) = }")
#
# part_a_instructions(instructions)
#

a = C(min=P(x=-1, y=-1, z=-1), max=P(x=1, y=1, z=1))
b = C(min=P(x=0, y=0, z=0), max=P(x=0, y=5, z=0))

c.print(f"{a.intersection(b) = }")

c.rule(f"FINISH {time.perf_counter() - start_time}")

