import modulefinder
import operator
import string
import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import reduce
from pathlib import PurePath, PurePosixPath
from typing import List, Dict

import networkx
import rich.console
from aocd.models import Puzzle
from more_itertools import chunked
from networkx import shortest_path
from rich import print

YEAR = 2022
DAY = 13

console = rich.console.Console()
puzzle = Puzzle(year=YEAR, day=DAY)
console.rule(
    f"{puzzle.title} ({YEAR}-{DAY})"
)  # ##########################################################
data = puzzle.input_data
# data = puzzle.example_data
data = data.replace("[", "tuple([")
data = data.replace("]", "])")


def isint(i):
    return isinstance(i, int)


def istup(i):
    return isinstance(i, tuple)


class State(Enum):
    VALID = auto()
    INVALID = auto()
    CONT = auto()


VALID = State.VALID
INVALID = State.INVALID
CONT = State.CONT


def compare(left, right):
    if isint(left) and isint(right):
        if left == right:
            return CONT
        elif left < right:
            return VALID
        else:
            return INVALID
    elif istup(left) and istup(right):
        if not left and right:
            return VALID
        elif left and not right:
            return INVALID
        elif not left and not right:
            return CONT
        else:
            r = compare(left[0], right[0])
            if r != CONT:
                return r
            else:
                return compare(left[1:], right[1:])
    elif istup(left) and isint(right):
        return compare(left, tuple([right]))
    elif isint(left) and istup(right):
        return compare(tuple([left]), right)


# Part 1
all_packets = []
in_the_right_order = []
for g, group in enumerate(data.split("\n\n")):
    index = g + 1
    left, right = [eval(line) for line in group.strip().splitlines()]
    all_packets.append(left)
    all_packets.append(right)
    result = compare(left, right)
    if result is VALID:
        in_the_right_order.append(index)
    print(f"result for {index=}, {result=}")
print(f"{in_the_right_order=}")
puzzle.answer_a = sum(in_the_right_order)

TWO = (2,)
SIX = (6,)

# part 2
class SortablePacket:
    def __init__(self, packet):
        self.packet = packet

    def __lt__(self, other):
        r = compare(self.packet, other.packet)
        if r is VALID:
            return True
        else:
            return False

    def __repr__(self):
        return f"SortablePacket(packet={self.packet!r})"


all_sortable_packets = [SortablePacket(packet) for packet in all_packets]
all_sortable_packets.append(SortablePacket(SIX))
all_sortable_packets.append(SortablePacket(TWO))
sorted_packets = sorted(all_sortable_packets)
print(sorted_packets)

for p, packet in enumerate(sorted_packets):
    if packet.packet == TWO:
        two_location = p + 1
    if packet.packet == SIX:
        six_location = p + 1

print(f"{two_location=}, {six_location=}")
puzzle.answer_b = two_location * six_location
console.rule("END")  # ##########################################################
