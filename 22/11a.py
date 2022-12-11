import modulefinder
from collections import defaultdict, deque
from dataclasses import dataclass, field
from pathlib import PurePath, PurePosixPath
from typing import List

import rich.console
from aocd.models import Puzzle
from more_itertools import chunked
from rich import print

YEAR = 2022
DAY = 11

console = rich.console.Console()
puzzle = Puzzle(year=YEAR, day=DAY)
console.rule(
    f"{puzzle.title} ({YEAR}-{DAY})"
)  # ##########################################################
data = puzzle.input_data
# data = puzzle.example_data
print(data)


@dataclass
class Monkey:
    id: int
    items: List[int]
    operation: str
    test_divisible_by: int
    if_true: int
    if_false: int
    investigations: int = 0

    def turn(self, monkeys: "List[Monkey]"):
        while self.items:
            item = self.items.pop(0)
            self.investigations += 1
            new_worry: int = eval(self.operation, dict(old=item))
            new_worry //= 3
            destination: int
            if new_worry % self.test_divisible_by == 0:
                destination = self.if_true
            else:
                destination = self.if_false
            print(
                f"Monkey {self.id} throws item with {new_worry} to Monkey {destination}"
            )
            monkeys[destination].items.append(new_worry)

    @classmethod
    def parse(cls, s):
        lines = s.split("\n")
        id = int(lines[0].split(":")[0].split()[1])
        items = [int(i) for i in lines[1].split(":")[1].split(", ")]
        operation = lines[2].split("=")[1].strip()
        test_divisible_by = int(lines[3].split()[-1])
        if_true = int(lines[4].split()[-1])
        if_false = int(lines[5].split()[-1])
        return Monkey(id, items, operation, test_divisible_by, if_true, if_false)


def round(monkeys):
    for monkey in monkeys:
        monkey.turn(monkeys)


monkeys = []
for monkey_spec in data.strip().split("\n\n"):
    monkeys.append(Monkey.parse(monkey_spec))

print(monkeys)
ROUNDS = 20
for i in range(ROUNDS):
    round(monkeys)
print(monkeys)

cheekiest_monkey, cheekier_monkey = sorted(monkeys, key=lambda x: -x.investigations)[:2]
monkey_business = cheekier_monkey.investigations * cheekiest_monkey.investigations

console.rule("END")  # ##########################################################
puzzle.answer_a = monkey_business
# puzzle.answer_b = "EKRHEPUZ"
