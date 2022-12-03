from enum import Enum, auto, IntEnum
from itertools import islice

from aocd.transforms import lines

YEAR = 2022
DAY = 3
PART = "b"

import time
from aocd import get_data, submit
from rich.console import Console

answer = None
c = Console()
start_time = time.perf_counter()
data = get_data(year=YEAR, day=DAY)
c.rule(f"Advent of Code {YEAR}-{DAY}{PART}")

def batched(iterable, n):
    "Batch data into lists of length n. The last batch may be shorter."
    # copied from https://docs.python.org/3/library/itertools.html#itertools-recipes
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while (batch := list(islice(it, n))):
        yield batch

###################################################################################
def priority(i):
    return 27 + ord(i) - ord("A") if i.isupper() else 1 + ord(i) - ord("a")

def intersected(group):
    a, b, c = set(group[0]), set(group[1]), set(group[2])
    intersection = a.intersection(b).intersection(c).pop()
    return priority(intersection)

groups = list(batched(lines(data), 3))
answer = sum(intersected(group) for group in groups)

print("answer", answer)
####################################################################################
c.rule("Finished")

submit(year=YEAR, day=DAY, part=PART, answer=answer)
