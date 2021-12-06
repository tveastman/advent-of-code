YEAR = 2021
DAY = 6

import time

start_time = time.perf_counter()

from aocd import get_data, submit
from rich.console import Console

data = get_data(year=YEAR, day=DAY)

# data = "3,4,3,1,2"

c = Console()
c.rule("START")

internal_timers = [0] * 9
for internal_timer in data.split(","):
    internal_timers[int(internal_timer)] += 1


def iterate(internal_timers):
    new_internal_timers = [0] * 9
    for i in range(1, len(internal_timers)):
        new_internal_timers[i - 1] = internal_timers[i]
    new_internal_timers[6] += internal_timers[0]
    new_internal_timers[8] += internal_timers[0]
    return new_internal_timers


# DAYS = 80  #  part a
DAYS = 256  # part b

c.print(0, internal_timers)
for i in range(DAYS):
    internal_timers = iterate(internal_timers)
    print(i + 1, internal_timers, sum(internal_timers))


c.rule(f"FINISH {time.perf_counter() - start_time}")

# submit(sum(internal_timers), day=6, part="a", year="2021")  # part a
submit(sum(internal_timers), day=6, part="b", year="2021")  # part b
