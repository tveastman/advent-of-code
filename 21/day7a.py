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

positions = [int(i) for i in data.split(",")]
positions.sort()
median = positions[len(positions) // 2]
c.print(sorted(positions))
c.print(f"{median = }")

fuel_per_crab = [abs(position - median) for position in positions]
c.print("fuel per crab", fuel_per_crab)
fuel_sum = sum(fuel_per_crab)
c.print(f"{fuel_sum = }")


c.rule(f"FINISH {time.perf_counter() - start_time}")

submit(fuel_sum, day=DAY, part="a", year=YEAR)
# submit(sum(internal_timers), day=6, part="b", year="2021")  # part b
