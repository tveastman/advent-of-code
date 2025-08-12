
YEAR = 2022
DAY = 2
PART = "b"

import time
from aocd import get_data, submit
from rich.console import Console

c = Console()
start_time = time.perf_counter()
data = get_data(year=YEAR, day=DAY)
c.rule(f"Advent of Code {YEAR}-{DAY}{PART}")
####################################################################################

example = """A Y
B X
C Z
"""

rock, paper, scissors = 1, 2, 3
lose, draw, win = 0, 3, 6

# X = LOSE
# Y = DRAW
# Z = WIN
outcomes = {
    ("A", "X"): scissors + lose,
    ("A", "Y"): rock + draw,
    ("A", "Z"): paper + win,
    ("B", "X"): rock + lose,
    ("B", "Y"): paper + draw,
    ("B", "Z"): scissors + win,
    ("C", "X"): paper + lose,
    ("C", "Y"): scissors + draw,
    ("C", "Z"): rock + win,
}

parsed = [tuple(i.split()) for i in data.strip().split("\n")]
print(parsed)
results = [outcomes[i] for i in parsed]
print(results)
answer = sum(results)
print("answer", answer)
####################################################################################
c.rule("Finished")

submit(year=YEAR, day=DAY, part=PART, answer=answer)
