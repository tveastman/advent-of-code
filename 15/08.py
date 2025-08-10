import rich.console
from aocd.models import Puzzle
from collections import defaultdict
from itertools import batched
import re
import typing
from attrs import define
import cattrs
from functools import partial, cache
import pyparsing as pp
import operator

YEAR = 2015
DAY = 8

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")

example = puzzle.examples[0]
# inputs = example.input_data.split()
inputs = puzzle.input_data.split()
print(inputs)

from ast import literal_eval

sum_raw = 0
sum_eval = 0
for input in inputs:
    raw_length = len(input)
    evaluated = literal_eval(input)
    evaluated_length = len(evaluated)
    print(f"{raw_length=} {evaluated_length=} {evaluated=!r} {input=!r}")
    sum_raw += len(input)
    sum_eval += evaluated_length

result = sum_raw - sum_eval
print(f"{result=}")
puzzle.answer_a = result

c.rule()


def encode(s: str) -> str:
    output: list[str] = []
    for char in s:
        if char == r'"':
            output.append(r"\"")
        elif char == "\\":
            output.append("\\\\")
        else:
            output.append(char)
    print(output)
    return '"' + "".join(output) + '"'


sum_raw = 0
sum_encoded = 0
for input in inputs:
    sum_raw += len(input)
    sum_encoded += len(encode(input))

puzzle.answer_b = sum_encoded - sum_raw
