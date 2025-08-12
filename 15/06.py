import rich.console
from aocd.models import Puzzle
import re
from attrs import frozen
import cattrs

YEAR = 2015
DAY = 6

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")

from array import array


class Grid:
    y_max: int
    x_max: int
    grid: array

    def __init__(self, x_max, y_max):
        self.x_max = x_max
        self.y_max = y_max
        self.grid = array("b", bytearray(self.x_max * self.y_max))

    def location(self, x: int, y: int) -> int:
        result = y * self.x_max + x
        return result

    def on(self, from_x, from_y, to_x, to_y):
        for y in range(from_y, to_y + 1):
            for x in range(from_x, to_x + 1):
                l = self.location(x, y)
                self.grid[l] = 1

    def off(self, from_x, from_y, to_x, to_y):
        for y in range(from_y, to_y + 1):
            for x in range(from_x, to_x + 1):
                l = self.location(x, y)
                self.grid[l] = 0

    def toggle(self, from_x, from_y, to_x, to_y):
        for y in range(from_y, to_y + 1):
            for x in range(from_x, to_x + 1):
                l = self.location(x, y)
                self.grid[l] = not (self.grid[l])

    def __str__(self):
        output = []
        for y in range(self.y_max):
            for x in range(self.x_max):
                location = self.location(x, y)
                output.append("*" if self.grid[location] else " ")
            output.append("\n")
        return "".join(output)


class GridPartB(Grid):
    def on(self, from_x, from_y, to_x, to_y):
        for y in range(from_y, to_y + 1):
            for x in range(from_x, to_x + 1):
                l = self.location(x, y)
                self.grid[l] += 1

    def off(self, from_x, from_y, to_x, to_y):
        for y in range(from_y, to_y + 1):
            for x in range(from_x, to_x + 1):
                l = self.location(x, y)
                if self.grid[l] > 0:
                    self.grid[l] -= 1

    def toggle(self, from_x, from_y, to_x, to_y):
        for y in range(from_y, to_y + 1):
            for x in range(from_x, to_x + 1):
                l = self.location(x, y)
                self.grid[l] += 2


grid = Grid(1000, 1000)
grid_part_b = GridPartB(1000, 1000)

parser = re.compile(
    r"""
    (?P<command>\D+)\ 
    (?P<from_x>\d+),
    (?P<from_y>\d+)\ through\ 
    (?P<to_x>\d+),
    (?P<to_y>\d+)
""",
    re.VERBOSE,
)



@frozen
class Command:
    command: str
    from_x: int
    from_y: int
    to_x: int
    to_y: int


input = puzzle.input_data.split("\n")

for line in input:
    match = parser.match(line)
    c = cattrs.structure(match.groupdict(), Command)
    if c.command == "turn on":
        grid.on(c.from_x, c.from_y, c.to_x, c.to_y)
        grid_part_b.on(c.from_x, c.from_y, c.to_x, c.to_y)
    elif c.command == "turn off":
        grid.off(c.from_x, c.from_y, c.to_x, c.to_y)
        grid_part_b.off(c.from_x, c.from_y, c.to_x, c.to_y)
    elif c.command == "toggle":
        grid.toggle(c.from_x, c.from_y, c.to_x, c.to_y)
        grid_part_b.toggle(c.from_x, c.from_y, c.to_x, c.to_y)

print(f"{grid.grid.count(1)=}")
puzzle.answer_a = grid.grid.count(1)

print(f"{sum(grid_part_b.grid)=}")
puzzle.answer_b = sum(grid_part_b.grid)
