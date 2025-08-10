from enum import Enum, auto, IntEnum

from aocd.transforms import lines

YEAR = 2022
DAY = 3
PART = "a"

import time
from aocd import get_data, submit
from rich.console import Console

c = Console()
start_time = time.perf_counter()
data = get_data(year=YEAR, day=DAY)
c.rule(f"Advent of Code {YEAR}-{DAY}{PART}")


###################################################################################
def priority(i):
    return 27 + ord(i) - ord("A") if i.isupper() else 1 + ord(i) - ord("a")


def intersected(line):
    l = len(line)
    a, b = set(line[: l // 2]), set(line[l // 2 :])
    intersected = a.intersection(b).pop()
    return priority(intersected)


answer = sum(intersected(line) for line in lines(data))
print("answer", answer)

####################################################################################
c.rule("Finished")

submit(year=YEAR, day=DAY, part=PART, answer=answer)
