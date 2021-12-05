import time
from math import copysign

start_time = time.perf_counter()

from collections import defaultdict
from dataclasses import dataclass

from aocd import data, submit
from rich.console import Console

c = Console()
c.rule("START")


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def step(self, x, y):
        return Point(self.x + x, self.y + y)


@dataclass(frozen=True)
class Line:
    a: Point
    b: Point

    def points_of_interest(self):
        x_delta = self.b.x - self.a.x
        y_delta = self.b.y - self.a.y
        x_step = int(copysign(1, x_delta)) if x_delta else 0
        y_step = int(copysign(1, y_delta)) if y_delta else 0
        c.print(f"line from {self.a} to {self.b} in steps of {x_step=}, {y_step=}")

        point = self.a
        points = [point]
        while point != self.b:
            point = point.step(x_step, y_step)
            points.append(point)
        return points


lines = []
for line in data.split("\n"):
    start, end = line.split("->")
    lines.append(
        Line(
            Point(*[int(i) for i in start.strip().split(",")]),
            Point(*[int(i) for i in end.strip().split(",")]),
        )
    )

overlap_counter = defaultdict(int)
doubles = 0
for l, line in enumerate(lines):
    print(f"Line {l}")
    for poi in line.points_of_interest():
        overlap_counter[poi] += 1
        if overlap_counter[poi] == 2:
            doubles += 1
c.print(f"{doubles = }")
c.rule(f"Finished in {time.perf_counter() - start_time}sec")

submit(str(doubles), day=5, part="b", year="2021")
