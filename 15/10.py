import rich.console
from aocd.models import Puzzle
from collections import defaultdict
import networkx as nx
import pyparsing as pp

YEAR = 2015
DAY = 10

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")


def lookandsay(s: str):
    chars = list(s)
    chars.reverse()
    output: list[str] = []
    while chars:
        sequence_char = chars.pop()
        count = 1
        while chars:
            n = chars.pop()
            if n == sequence_char:
                count += 1
            else:
                chars.append(n)
                break
        output.append(str(count))
        output.append(str(sequence_char))
    return "".join(output)


number = puzzle.input_data
for i in range(40):
    number = lookandsay(number)
    print(f"{len(number)=}")
puzzle.answer_a = len(number)

for i in range(10):
    number = lookandsay(number)
    print(f"{len(number)=}")
puzzle.answer_b = len(number)
