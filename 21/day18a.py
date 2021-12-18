from __future__ import annotations

import ast
import itertools
from dataclasses import dataclass
from typing import Tuple

import re

YEAR = 2021
DAY = 18

import time
from aocd import get_data, submit
from rich.console import Console

start_time = time.perf_counter()
c = Console()
data = get_data(year=YEAR, day=DAY)
c.rule("START")


def idx_explodable(sn_str) -> Tuple[int, int]:
    level, start = 0, 0

    for c, char in enumerate(sn_str):
        # print(c, char, level)
        if char == "[":
            level += 1
            if level == 5:
                start = c
        if char == "]":
            if level == 5:
                return start, c
            else:
                level -= 1
    return 0, 0


rn_re = re.compile(r"(\d+)")


def is_rn(sn):
    return isinstance(sn, int)


def explode(sn):
    sn_str = str(sn)
    start, end = idx_explodable(sn_str)
    # print(f"{start=}, {end=}")
    if not end:
        return sn
    left, center, right = sn_str[:start], sn_str[start : end + 1], sn_str[end + 1 :]
    add_left, add_right = ast.literal_eval(center)
    # print(f"{add_left = }, {add_right = }")

    left_chunks = rn_re.split(left)
    if len(left_chunks) > 1:
        left_chunks[-2] = str(int(left_chunks[-2]) + add_left)
    right_chunks = rn_re.split(right)
    if len(right_chunks) > 1:
        right_chunks[1] = str(int(right_chunks[1]) + add_right)
    reconstructed_string = "".join(left_chunks) + "0" + "".join(right_chunks)
    # print(f"{reconstructed_string= }")
    result = ast.literal_eval(reconstructed_string)
    # c.print("after explode", result)
    return result


def split(sn):
    sn_str = str(sn)
    tokens = rn_re.split(sn_str)
    # c.print(tokens)
    for i in range(1, len(tokens), 2):
        value = int(tokens[i])
        if value >= 10:
            left = value // 2
            right = value - left
            tokens[i] = f"[{left}, {right}]"
            break
    result = ast.literal_eval("".join(tokens))
    # c.print("after split: ", result)
    return result


def add(sn1, sn2):
    added = [sn1, sn2]
    # c.print("after addition", added)
    reduced = reduce(added)
    return reduced


def reduce(sn):
    while True:
        exploded_sn = explode(sn)
        if exploded_sn != sn:
            sn = exploded_sn
            continue
        split_sn = split(sn)
        if split_sn != sn:
            sn = split_sn
            continue
        else:
            return split_sn


def magnitude(sn):
    if is_rn(sn):
        return sn
    else:
        return 3 * magnitude(sn[0]) + 2 * magnitude(sn[1])


def add_list(sns):
    current_sum = sns[0]
    for sn in sns[1:]:
        current_sum = add(current_sum, sn)
    return current_sum
    # c.print("final sum", current_sum)
    # c.print("magnitude", magnitude(current_sum))


def add_text_list(list_as_text):
    sns = []
    for line in list_as_text.strip().split("\n"):
        sns.append(ast.literal_eval(line))
    return add_list(sns)


def parse(list_as_text):
    sns = []
    for line in list_as_text.strip().split("\n"):
        sns.append(ast.literal_eval(line))
    return sns


assert explode([[[[[9, 8], 1], 2], 3], 4]) == [[[[0, 9], 2], 3], 4]
assert explode([7, [6, [5, [4, [3, 2]]]]]) == [7, [6, [5, [7, 0]]]]
assert explode([[6, [5, [4, [3, 2]]]], 1]) == [[6, [5, [7, 0]]], 3]
assert explode([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]) == [
    [3, [2, [8, 0]]],
    [9, [5, [4, [3, 2]]]],
]
assert explode([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]) == [
    [3, [2, [8, 0]]],
    [9, [5, [7, 0]]],
]
assert split([[[[0, 7], 4], [15, [0, 13]]], [1, 1]]) == [
    [[[0, 7], 4], [[7, 8], [0, 13]]],
    [1, 1],
]
assert split([[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]]) == [
    [[[0, 7], 4], [[7, 8], [0, [6, 7]]]],
    [1, 1],
]
assert add([[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]) == [
    [[[0, 7], 4], [[7, 8], [6, 0]]],
    [8, 1],
]
assert magnitude([[1, 2], [[3, 4], 5]]) == 143
assert (
    magnitude([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]])
    == 3488
)
assert add_list([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]) == [
    [[[1, 1], [2, 2]], [3, 3]],
    [4, 4],
]

assert (
    add_list(
        [
            [1, 1],
            [2, 2],
            [3, 3],
            [4, 4],
            [5, 5],
        ]
    )
    == [[[[3, 0], [5, 3]], [4, 4]], [5, 5]]
)

assert (
    add_text_list(
        """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]
"""
    )
    == [[[[5, 0], [7, 4]], [5, 5]], [6, 6]]
)

assert (
    add_text_list(
        """
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
"""
    )
    == [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
)

# part a
final_answer = add_text_list(data)
c.print(f"{final_answer = }")
c.print(f"{magnitude(final_answer) = }")

# part b
sns = parse(data)
c.print(sns)
best_magnitude = 0
all_permutations = list(itertools.permutations(sns, 2))
c.print(f"{len(all_permutations)}")
perm_count = 0
for a, b in all_permutations:
    perm_count += 1
    current_magnitude = magnitude(add(a, b))
    if current_magnitude > best_magnitude:
        best_magnitude = current_magnitude
        print(f"after {perm_count} the best magnitude is {best_magnitude}")


c.rule(f"FINISH {time.perf_counter() - start_time}")
