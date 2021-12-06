import time

start_time = time.perf_counter()

from collections import defaultdict
from dataclasses import dataclass

from aocd import get_data, submit
from rich.console import Console

data = get_data(year=2021, day=5)

c = Console()
c.rule("START")


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Line:
    a: Point
    b: Point

    def points_of_interest(self):
        if self.a.x == self.b.x:
            # vertical
            start, end = sorted([self.a.y, self.b.y])
            return [Point(self.a.x, y) for y in range(start, end + 1)]
        elif self.a.y == self.b.y:
            # horizontal
            start, end = sorted([self.a.x, self.b.x])
            return [Point(x, self.a.y) for x in range(start, end + 1)]
        else:
            c.print(f"Ignoring kinky line {line}")
            return []


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
for line in lines:
    for poi in line.points_of_interest():
        overlap_counter[poi] += 1
        if overlap_counter[poi] == 2:
            doubles += 1
c.print(f"{doubles = }")
c.rule(f"Finished in {time.perf_counter() - start_time}sec")

submit(str(doubles), day=5, part="a", year="2021")
