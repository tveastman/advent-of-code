import typing

import attrs
import re
import rich.console
from aocd.models import Puzzle
import array
import itertools

YEAR = 2015
DAY = 18

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")

example = """
.#.#.#
...##.
#....#
..#...
#.#..#
####..
"""


def strip_whitespace(s):
    return "".join(s.split())


@attrs.frozen
class Grid:
    rows: int
    columns: int
    grid: array.array

    def coords(self, i):
        row = i // self.columns
        column = i % self.columns
        return row, column

    def at(self, row, column):
        if 0 <= row < self.rows and 0 <= column < self.columns:
            return self.grid[row * self.columns + column]
        else:
            return None

    def print(self):
        for batch in itertools.batched(self.grid, self.columns):
            print("".join(batch))

    def neighbours(self, row, column):
        n = []
        for r in [-1, 0, 1]:
            for c in [-1, 0, 1]:
                if r == 0 and c == 0:
                    continue
                c = self.at(row + r, column + c)
                if c:
                    n.append(c)
        return n

    def step(self, corners_always_on=False):
        new_grid = array.array("u")
        for r in range(self.rows):
            for c in range(self.columns):
                n = self.neighbours(r, c)
                v = self.at(r, c)
                if v == "#":
                    new = "#" if n.count("#") in (2, 3) else "."
                else:
                    new = "#" if n.count("#") == 3 else "."
                if corners_always_on:
                    if (r, c) in [
                        (0, 0),
                        (0, self.columns - 1),
                        (self.rows - 1, 0),
                        (self.rows - 1, self.columns - 1),
                    ]:
                        new = "#"
                new_grid.append(new)
        return Grid(self.rows, self.columns, new_grid)


g = Grid(6, 6, array.array("u", strip_whitespace(example)))
print("initial state")
g.print()
for i in range(4):
    print(f"step {i + 1}")
    g = g.step()
    g.print()

g = Grid(100, 100, array.array("u", strip_whitespace(puzzle.input_data)))

for i in range(100):
    g = g.step()
print("done")
g.print()
on_count = g.grid.count("#")
print(f"{on_count=}")
puzzle.answer_a = on_count


g = Grid(100, 100, array.array("u", strip_whitespace(puzzle.input_data)))
for i in range(100):
    g = g.step(corners_always_on=True)
print("done")
g.print()
on_count = g.grid.count("#")
print(f"{on_count=}")
puzzle.answer_b = on_count
