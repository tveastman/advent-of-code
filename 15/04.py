import rich.console
from aocd.models import Puzzle
from collections import defaultdict

YEAR = 2015
DAY = 4

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")

log(f"{puzzle.input_data=}")
from hashlib import md5

secret_key = puzzle.input_data
# secret_key = "pqrstuv"

start = md5()
start.update(secret_key.encode())
counter = 0
while True:
    h = start.copy()
    h.update(str(counter).encode())
    if h.hexdigest().startswith("00000"):
        break
    counter += 1
log(f"{counter=}")
puzzle.answer_a = counter


start = md5()
start.update(secret_key.encode())
counter = 0
while True:
    h = start.copy()
    h.update(str(counter).encode())
    if h.hexdigest().startswith("000000"):
        break
    counter += 1
log(f"{counter=}")
puzzle.answer_b = counter
