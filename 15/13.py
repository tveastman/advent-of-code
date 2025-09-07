import rich.console
from aocd.models import Puzzle

YEAR = 2015
DAY = 13

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")

import re

line_re = re.compile(
    r"(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)"
)

example = """Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
"""

# lines = example.splitlines()
lines = puzzle.input_data.splitlines()

type Config = dict[tuple[str, str], int]
config: Config = {}
attendees: set[str] = set()
for line in lines:
    groups = line_re.match(line).groups()
    change = int(groups[2]) if groups[1] == "gain" else int(groups[2]) * -1
    config[groups[0], groups[3]] = change
    attendees.add(groups[0])

print(config)
print(attendees)


def score(arrangement: tuple[str, ...], config: Config) -> int:
    len_arrangement = len(arrangement)
    score = 0
    for i in range(len_arrangement):
        l = (i - 1) % len_arrangement
        r = (i + 1) % len_arrangement
        score += (
            config[arrangement[i], arrangement[l]]
            + config[arrangement[i], arrangement[r]]
        )
    return score


def score_b(arrangement: tuple[str, ...], config: Config) -> int:
    len_arrangement = len(arrangement)
    score = 0
    for i in range(len_arrangement):
        l = i - 1
        r = i + 1
        if r != len_arrangement:
            score += config[arrangement[i], arrangement[r]]
        if l != -1:
            score += config[arrangement[i], arrangement[l]]
    return score


import itertools

max_score = 0
for permutation in itertools.permutations(list(attendees)):
    # print(f"{permutation=}, {score(permutation, config)}")
    new_score = score(permutation, config)
    max_score = new_score if new_score > max_score else max_score
print(f"{max_score=}")
puzzle.answer_a = max_score

max_score = 0
for permutation in itertools.permutations(list(attendees)):
    # print(f"{permutation=}, {score(permutation, config)}")
    new_score = score_b(permutation, config)
    max_score = new_score if new_score > max_score else max_score
print(f"{max_score=}")
puzzle.answer_b = max_score
