YEAR = 2022
DAY = 1
PART = "a"

import time
from aocd import get_data, submit
from rich.console import Console

c = Console()
start_time = time.perf_counter()
data = get_data(year=YEAR, day=DAY)
c.rule("Advent of Code")
groups = [j.split() for j in data.split('\n\n')]
sums = [sum(int(i) for i in j) for j in groups]
largest_sum = max(sums)
c.rule("Finished")
answer = largest_sum
submit(year=YEAR, day=DAY, part=PART, answer=answer)