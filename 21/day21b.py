from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

YEAR = 2021
DAY = 21

import time
from aocd import get_data
from rich.console import Console

start_time = time.perf_counter()
c = Console()
print = c.print

data = get_data(year=YEAR, day=DAY)

c.rule("START")
print(data)


def smod(value, n, modulo):
    return (value - n) % (modulo - (n - 1)) + n


@dataclass(frozen=True)
class Player:
    pos: int
    score: int = 0


def go(p1, p2, universes, current_universe_count):
    for a in range(1, 3 + 1):
        for b in range(1, 3 + 1):
            for c in range(1, 3 + 1):
                roll = a + b + c
                pos = smod(p1.pos + roll, 1, 10)
                score = p1.score + pos
                new_player1 = Player(pos, score)
                if new_player1.score >= 21:
                    universes[(new_player1, p2)] += current_universe_count
                else:
                    for d in range(1, 3 + 1):
                        for e in range(1, 3 + 1):
                            for f in range(1, 3 + 1):
                                roll = d + e + f
                                pos = smod(p2.pos + roll, 1, 10)
                                score = p2.score + pos
                                new_player2 = Player(pos, score)
                                universes[(new_player1, new_player2)] += (
                                    current_universe_count
                                )


p1 = Player(pos=6)
p2 = Player(pos=9)

list_of_states = [{(p1, p2): 1}]
for i in range(1, 15):
    new_universes = defaultdict(int)
    current_universes = list_of_states[i - 1]
    list_of_states.append(new_universes)
    for k, v in current_universes.items():
        player1, player2 = k
        if player1.score < 21 and player2.score < 21:
            go(player1, player2, new_universes, v)
    print(f"turn {i}, {len(new_universes) = }")

# print(list_of_states)
# print(list(list_of_states[-1])[:100])

p1_wins = 0
p2_wins = 0
for i in list_of_states:
    for j, k in i.items():
        p1, p2 = j
        if p1.score >= 21:
            p1_wins += k
        elif p2.score >= 21:
            p2_wins += k

print(p1_wins, p2_wins, p1_wins > p2_wins)

# print(list_of_states[-1])

c.rule(f"FINISH {time.perf_counter() - start_time}")
