import rich.console
from aocd.models import Puzzle

YEAR = 2015
DAY = 14

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")

def distance(t: int, v: int, f: int, r: int):
    cycle_duration = f + r
    completed_cycles = t // cycle_duration
    remaining_duration = t - (completed_cycles * cycle_duration)
    remainder_flight_seconds = min(f, remaining_duration)
    result = (completed_cycles * v * f) + (remainder_flight_seconds * v)
    return result

import re
line_re = re.compile(f"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")

max_distance = 0
TIME_POINT = 2503
for line in puzzle.input_data.splitlines():
    name, v, f, r = line_re.match(line).groups()
    current_distance = distance(2503, int(v), int(f), int(r))
    if current_distance > max_distance:
        max_distance = current_distance
print(f"{max_distance=}")
puzzle.answer_a = max_distance

c.rule()