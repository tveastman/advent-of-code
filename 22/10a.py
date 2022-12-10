from collections import defaultdict, deque
from dataclasses import dataclass, field
from pathlib import PurePath, PurePosixPath
from typing import List

import rich.console
from aocd.models import Puzzle
from more_itertools import chunked
from rich import print

YEAR = 2022
DAY = 10

console = rich.console.Console()
puzzle = Puzzle(year=YEAR, day=DAY)
console.rule(
    f"{puzzle.title} ({YEAR}-{DAY})"
)  # ##########################################################
data = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""


@dataclass
class CPU:
    x: int = 1
    c: int = 0
    s: int = 0
    crt: str = ""

    def cycle(self):
        c, x = self.c + 1, self.x
        if (c + 20) % 40 == 0:
            s = c * x
            self.s += s
            print(f"{c=}, {x=}, {s=}, {self.s=}")

        crt_pos = (c - 1) % 40
        if x - 1 == crt_pos or x == crt_pos or x + 1 == crt_pos:
            self.crt += "#"
        else:
            self.crt += "."
        self.c += 1

    def noop(self):
        self.cycle()

    def addx(self, a: int):
        self.cycle()
        self.cycle()
        self.x += a


data = puzzle.input_data
cpu = CPU()
for line in data.strip().splitlines():
    tokens = line.split()
    print(tokens)
    if tokens[0] == "noop":
        cpu.noop()
    elif tokens[0] == "addx":
        cpu.addx(int(tokens[1]))
    print(cpu)

# print(cpu.crt)

for line in chunked(cpu.crt, 40):
    print("".join(line))


console.rule("END")  # ##########################################################
puzzle.answer_a = cpu.s
puzzle.answer_b = "EKRHEPUZ"
