import humanize
import rich.console
from aocd.models import Puzzle
from collections import defaultdict
import networkx as nx
import pyparsing as pp


YEAR = 2023
DAY = 1

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")


def handle_line(line, targets):
    found = []
    for i in range(len(line)):
        for t in targets:
            if line[i : i + len(t)] == t:
                found.append(t)
    return found


digit_sum = 0
for line in puzzle.input_data.splitlines():
    found = handle_line(line, list("123456789"))
    first, last = found[0], found[-1]
    digit_sum += int(first + last)
puzzle.answer_a = digit_sum

s = "1 2 3 4 5 6 7 8 9 one two three four five six seven eight nine".split()
decimals, words = s[:9], s[9:]
w2d = dict(zip(words, decimals))
print(decimals, words, w2d)

digit_sum = 0
for line in puzzle.input_data.splitlines():
    found = handle_line(line, s)
    first, last = found[0], found[-1]
    print(first, last)
    first = first if len(first) == 1 else w2d[first]
    last = last if len(last) == 1 else w2d[last]
    print(first, last)
    digit_sum += int(first + last)
puzzle.answer_b = digit_sum
