from dataclasses import dataclass

import rich.console
from aocd.models import Puzzle

YEAR = 2022
DAY = 4

c = rich.console.Console()
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(
    f"{puzzle.title} ({YEAR}-{DAY})"
)  # ##########################################################


@dataclass
class Assignment:
    s: int
    f: int

    def contains(self, other):
        return self.s <= other.s and other.f <= self.f

    def fully_contains(self, other):
        return self.contains(other) or other.contains(self)

    def overlaps(self, other):
        s = set(range(self.s, self.f + 1))
        o = set(range(other.s, other.f + 1))
        return bool(s & o)

    @classmethod
    def parse(cls, spec):
        ends = spec.strip().split("-")
        if len(ends) == 1:
            return cls(int(ends[0]), int(ends[0]))
        else:
            return cls(int(ends[0]), int(ends[1]))


fully_contains = 0
overlaps = 0
for line in puzzle.input_data.splitlines():
    a, b = line.strip().split(",")
    a, b = Assignment.parse(a), Assignment.parse(b)
    print(line, a, b)
    if a.fully_contains(b):
        fully_contains += 1
        print("fully contains")
    if a.overlaps(b):
        overlaps += 1
        print("overlaps")

print(f"{fully_contains=}")
print(f"{overlaps=}")
c.rule()  # ##########################################################
puzzle.answer_a = fully_contains
puzzle.answer_b = overlaps
