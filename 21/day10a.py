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


score = {
    ")": 3,
    "]": 57,
    "}": 1_197,
    ">": 25_137,
}
closes = {i: j for i, j in chunked("()[]{}<>", 2)}
c.print(closes)

data = get_data(year=YEAR, day=DAY)
# data = """[({(<(())[]>[[{[]{<()<>>
# [(()[<>])]({[<{<<[]>>(
# {([(<{}[<>[]}>{[]{[(<()>
# (((({<>}<{<{<>}{[]{[]{}
# [[<[([]))<([[{}[[()]]]
# [{[{({}]{}}([{[{{{}}([]
# {<[[]]>}<{[{[{[]{()[[[]
# [<(<(<(<{}))><([]([]()
# <{([([[(<>()){}]>(<<{{
# <{([{{}}[<[[[<>{}]]]>[]]
# """
print(data)


def corrupt_line_score(line):
    print(f"{line = !r}")
    stack = []

    for c, chr in enumerate(line):
        if chr in "([{<":
            stack.append(chr)
        else:
            match = stack.pop()
            if closes[match] != chr:
                return score[chr]
    return 0


total_score = 0
for line in data.strip().split():
    total_score += corrupt_line_score(line.strip())

c.print(f"{total_score = }")
answer = total_score
c.rule(f"FINISH {time.perf_counter() - start_time}")

submit(answer, day=DAY, part="a", year=YEAR)
