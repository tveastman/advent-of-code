from functools import lru_cache

YEAR = 2021
DAY = 7

import time

start_time = time.perf_counter()

from aocd import get_data, submit
from rich.console import Console

data = get_data(year=YEAR, day=DAY)

# data = "16,1,2,0,4,2,7,1,2,14"

c = Console()
c.rule("START")


@lru_cache(maxsize=None)
def fuel_cost(distance):
    return sum(range(1, abs(distance) + 1))


def total_fuel_cost(positions, destination):
    return sum(fuel_cost(position - destination) for position in positions)


crab_positions = [int(i) for i in data.split(",")]
crab_positions.sort()
min_pos, max_pos = min(crab_positions), max(crab_positions)
all_positions = range(min_pos, max_pos + 1)

# (commentary) I spent 10 minutes trying to work out how to use
# 'bisect' to do a binary search, because I assumed it would take
# too long to calculate the fuel cost for every possible position.
# but it actually only took a half a second to do them all so ¯\_(ツ)_/¯
all_fuel_costings = [total_fuel_cost(crab_positions, i) for i in all_positions]
answer = min(all_fuel_costings)

print(f"{answer = }")

c.rule(f"FINISH {time.perf_counter() - start_time}")

submit(answer, day=DAY, part="b", year=YEAR)
