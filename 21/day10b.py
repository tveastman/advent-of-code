from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations, product, permutations, combinations_with_replacement
from typing import Tuple, Set, List

from more_itertools import chunked

YEAR = 2021
DAY = 10

import time
from aocd import get_data, submit
from rich.console import Console

start_time = time.perf_counter()
c = Console()
c.rule("START")

lookup = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}
closes = {i: j for i, j in chunked("()[]{}<>", 2)}
c.print(closes)

data = get_data(year=YEAR, day=DAY)


def corrupt_line_score(line):
    print(f"{line = !r}")
    stack = []

    for c, chr in enumerate(line):
        if chr in "([{<":
            stack.append(chr)
        else:
            match = stack.pop()
            if closes[match] != chr:
                # Discard the corrupt lines
                return None
    stack.reverse()
    score = 0
    for chr in stack:
        score *= 5
        score += lookup[closes[chr]]
    return score


scores = []
for line in data.strip().split():
    scores.append(corrupt_line_score(line.strip()))
scores = [i for i in scores if i is not None]
scores.sort()
median = scores[len(scores) // 2]
print(f"{median = }")

answer = median
c.rule(f"FINISH {time.perf_counter() - start_time}")

submit(answer, day=DAY, part="b", year=YEAR)
