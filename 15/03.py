import rich.console
from aocd.models import Puzzle
from collections import defaultdict

YEAR = 2015
DAY = 3

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")

directions = {"^": 1j, "v": -1j, "<": -1, ">": 1}

location = 0
presents = defaultdict(int)
presents[location] += 1
for char in puzzle.input_data:
    location += directions[char]
    presents[location] += 1
puzzle.answer_a = len(presents)
log(f"{puzzle.answer_a=}")


presents = defaultdict(int)
instructions = list(puzzle.input_data)
santa_location, robo_location = 0, 0
presents[0] += 2
while instructions:
    instruction = directions[instructions.pop(0)]
    santa_location += instruction
    presents[santa_location] += 1
    instruction = directions[instructions.pop(0)]
    robo_location += instruction
    presents[robo_location] += 1
puzzle.answer_b = len(presents)
log(f"{puzzle.answer_b=}")
