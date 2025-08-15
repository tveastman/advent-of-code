import rich.console
from aocd.models import Puzzle


YEAR = 2016
DAY = 1

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")


import re

input = puzzle.input_data

re_instruction = re.compile(r"([LR])([\d]+),?")
velocity = 1j
position = 0

for instruction in input.split():
    print(repr(instruction))
    turn, distance = re_instruction.match(instruction).groups()
    distance = int(distance)
    if turn == "R":
        velocity *= -1j
    elif turn == "L":
        velocity *= 1j
    position += distance * velocity
print(int(position.imag + position.real))
puzzle.answer_a = int(position.imag + position.real)

position, velocity = 0, 1j
visited = set([position])

for instruction in input.split():
    print(repr(instruction))
    turn, distance = re_instruction.match(instruction).groups()
    distance = int(distance)
    if turn == "R":
        velocity *= -1j
    elif turn == "L":
        velocity *= 1j
    for step in range(distance):
        position = position + velocity
        if position in visited:
            print("we've been here before!")
            puzzle.answer_b = int(position.imag + position.real)
            import sys

            sys.exit(0)
        else:
            visited.add(position)
