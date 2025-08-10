import rich.console
from aocd.models import Puzzle
from collections import defaultdict
import networkx as nx
import pyparsing as pp

YEAR = 2015
DAY = 9

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")

name = pp.Word(pp.alphanums)
line = pp.Group(
    name
    + pp.Suppress(pp.Literal("to"))
    + name
    + pp.Suppress(pp.Literal("="))
    + pp.common.integer
    + pp.Suppress(pp.Optional(pp.LineEnd()))
)
lines = line[1, ...]

# parsed = lines.parse_string(puzzle.examples[0].input_data).as_list()
parsed = lines.parse_string(puzzle.input_data).as_list()

G = nx.Graph()

for start, end, weight in parsed:
    G.add_edge(start, end, weight=weight)

print(G)

path = nx.approximation.traveling_salesman.traveling_salesman_problem(
    G,
    cycle=False,
    weight="weight",
)
# print(path)

import itertools

min_distance = 1000
max_distance = 0
min_path = None
for permutation in itertools.permutations(G.nodes, 8):
    distance = nx.path_weight(G, permutation, weight="weight")
    if distance < min_distance:
        min_path = permutation
        min_distance = distance
    if distance > max_distance:
        max_distance = distance

print(f"{min_distance=}")
print(min_path)
puzzle.answer_a = min_distance
puzzle.answer_b = max_distance
