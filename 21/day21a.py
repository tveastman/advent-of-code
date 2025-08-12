from __future__ import annotations

from dataclasses import dataclass

YEAR = 2021
DAY = 21

import time
from aocd import get_data
from rich.console import Console

start_time = time.perf_counter()
c = Console()
print = c.print

data = get_data(year=YEAR, day=DAY)

c.rule("START")
print(data)


def smod(value, n, modulo):
    return (value - n) % (modulo - (n - 1)) + n


@dataclass
class DetermiDice:
    count: int = 0
    value: int = 100

    def roll(self):
        self.count += 1
        self.value = smod(self.value + 1, 1, 100)
        return self.value

    def nroll(self, n):
        return self.roll() + self.roll() + self.roll()


d = DetermiDice()


@dataclass
class Player:
    pos: int
    score: int = 0

    def go(self):
        r = d.nroll(3)
        self.pos = smod(self.pos + r, 1, 10)
        self.score += self.pos


p1 = Player(pos=6)
p2 = Player(pos=9)
d = DetermiDice()

while True:
    p1.go()
    if p1.score >= 1000:
        print(f"{p2.score * d.count = }")
        break
    p2.go()
    if p2.score >= 1000:
        print(f"{p1.score * d.count = }")
        break

c.rule(f"FINISH {time.perf_counter() - start_time}")
