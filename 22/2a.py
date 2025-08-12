
YEAR = 2022
DAY = 2
PART = "a"

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

# outcomes = {
#     ("A", "X"): rock + draw,
#     ("A", "Y"): rock + lose,
#     ("A", "Z"): rock + win,
#     ("B", "X"): paper + win,
#     ("B", "Y"): paper + draw,
#     ("B", "Z"): paper + lose,
#     ("C", "X"): scissors + lose,
#     ("C", "Y"): scissors + win,
#     ("C", "Z"): scissors + draw,
# }

# LOL, the above table is exactly backwards because I can't read.
outcomes = {
    ("A", "X"): rock + draw,
    ("A", "Y"): paper + win,
    ("A", "Z"): scissors + lose,
    ("B", "X"): rock + lose,
    ("B", "Y"): paper + draw,
    ("B", "Z"): scissors + win,
    ("C", "X"): rock + win,
    ("C", "Y"): paper + lose,
    ("C", "Z"): scissors + draw,
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
