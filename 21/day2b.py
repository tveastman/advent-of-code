from dataclasses import dataclass
from enum import Enum, auto

from rich import print


class Keyword(Enum):
    up = auto()
    down = auto()
    forward = auto()


@dataclass
class Statement:
    keyword: Keyword
    value: int


def parse(filename):
    instructions = []
    with open(filename) as f:
        for line in f:
            k, v = line.split()
            instructions.append(Statement(keyword=Keyword[k], value=int(v)))
    return instructions


@dataclass
class Sub:
    aim: int = 0
    depth: int = 0
    horizontal: int = 0

    def down(self, value: int) -> None:
        self.aim += value

    def up(self, value: int) -> None:
        self.aim -= value

    def forward(self, value: int):
        self.horizontal += value
        self.depth += self.aim * value

    @property
    def calculate(self):
        return self.horizontal * self.depth

    def instruct(self, statement):
        if statement.keyword is Keyword.down:
            self.down(statement.value)
        elif statement.keyword is Keyword.up:
            self.up(statement.value)
        elif statement.keyword is Keyword.forward:
            self.forward(statement.value)
        else:
            raise ValueError


instructions = parse("input-day2.txt")
sub = Sub()
for instruction in instructions:
    sub.instruct(instruction)
    print(instruction, sub, sub.calculate)
