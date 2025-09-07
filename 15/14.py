import typing

import attrs
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

line_re = re.compile(
    f"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds."
)

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


@attrs.frozen
class Reindeer:
    name: str
    velocity: int
    fly: int
    rest: int

    def distance_at(self, t: int) -> int:
        v, f, r = self.velocity, self.fly, self.rest
        cycle_duration = f + r
        completed_cycles = t // cycle_duration
        remaining_duration = t - (completed_cycles * cycle_duration)
        remainder_flight_seconds = min(f, remaining_duration)
        result = (completed_cycles * v * f) + (remainder_flight_seconds * v)
        return result

    @classmethod
    def leaders_at(cls, contestants: list[typing.Self], t: int) -> list[typing.Self]:
        top_distance = 0
        leaders = []
        for contestant in contestants:
            distance = contestant.distance_at(t)
            if distance == top_distance:
                leaders.append(contestant)
            if distance > top_distance:
                top_distance = distance
                leaders = [contestant]
        return leaders


contestants: list[Reindeer] = []
for line in puzzle.input_data.splitlines():
    name, v, f, r = line_re.match(line).groups()
    contestants.append(Reindeer(name, int(v), int(f), int(r)))

from collections import Counter

leader_counter = Counter()
for t in range(1, TIME_POINT + 1):
    leader_counter.update(Reindeer.leaders_at(contestants, t))

print(f"{leader_counter=}")
winner, winning_points = leader_counter.most_common(1)[0]
puzzle.answer_b = winning_points
