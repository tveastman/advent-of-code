from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Dict, Optional

import rich.console
from aocd.models import Puzzle
from rich import print
from sortedcontainers import SortedSet

YEAR = 2022
DAY = 14

console = rich.console.Console()
puzzle = Puzzle(year=YEAR, day=DAY)
console.rule(
    f"{puzzle.title} ({YEAR}-{DAY})"
)  # ##########################################################
data = puzzle.input_data
# data = puzzle.example_data
# print(data)


@dataclass(frozen=True, order=True)
class P:
    x: int
    y: int

    def __add__(self, other):
        return P(self.x + other.x, self.y + other.y)


DOWN = P(0, 1)
LEFT = P(-1, 0)
RIGHT = P(1, 0)


class S(Enum):
    AIR = auto()
    SAND = auto()
    ROCK = auto()
    ENDLESS_SCREAMING_VOID = auto()


class Cave:
    def __init__(self):
        self.points: Dict[P, S] = dict()
        self.heights: Dict[int, SortedSet] = dict()
        self.floor: Optional[int] = None

    def add(self, p, s):
        x, y = p.x, p.y
        self.points[p] = s
        if x not in self.heights:
            self.heights[x] = SortedSet([y])
        self.heights[p.x].add(p.y)

    def set_floor(self):
        DISTANCE = 2
        floor = 0
        for x, heights in self.heights.items():
            if heights and heights[-1] + DISTANCE > floor:
                floor = heights[-1] + DISTANCE
        self.floor = floor

    def draw_rock(self, p1: P, p2: P):
        x1, x2 = sorted([p1.x, p2.x])
        y1, y2 = sorted([p1.y, p2.y])
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                p = P(x, y)
                self.add(p, S.ROCK)

    def draw_rock_path(self, points: List[P]):
        for i in range(1, len(points)):
            p1, p2 = points[i - 1], points[i]
            self.draw_rock(p1, p2)

    def parse_input(self, data: str):
        for line in data.splitlines():
            points = []
            for token in line.split(" -> "):
                x, y = [int(i) for i in token.split(",")]
                p = P(x, y)
                points.append(p)
            # print(f"{points=}")
            self.draw_rock_path(points)

    def drop_grain(self, origin):
        if origin in self.points:
            print("origin blocked")
            return None
        x, y = origin.x, origin.y
        heights = self.heights.get(x)
        if not heights:
            if self.floor:
                loc = P(x, self.floor - 1)
                self.add(loc, S.SAND)
                return loc
            else:
                # falling into the endless screaming void
                return None
        index = self.heights[x].bisect_left(y)
        if index == len(heights):
            if self.floor:
                loc = P(x, self.floor - 1)
                self.add(loc, S.SAND)
                return loc
            else:
                # falling into the endless screaming void
                return None
        new_y = heights[index] - 1
        loc = P(x, new_y)
        down_left = loc + DOWN + LEFT
        down_right = loc + DOWN + RIGHT
        if not self.points.get(down_left):
            return self.drop_grain(down_left)
        elif not self.points.get(down_right):
            return self.drop_grain(down_right)
        else:
            self.add(loc, S.SAND)
            return loc


cave = Cave()
cave.parse_input(data)

ORIGIN = P(500, 0)
grains = 0
while True:
    result = cave.drop_grain(ORIGIN)
    # print(f"{result=}")
    if result:
        grains += 1
    else:
        break
print(f"{grains=}")
puzzle.answer_a = grains

# PART 2
cave.set_floor()
# print(cave.heights)
while True:
    result = cave.drop_grain(ORIGIN)
    # print(f"{result=}")
    if result:
        grains += 1
    else:
        break

print(f"{grains=}")
puzzle.answer_b = grains

console.rule("END")  # ##########################################################
