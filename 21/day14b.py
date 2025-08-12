from __future__ import annotations

from collections import defaultdict
import re
from typing import Tuple, DefaultDict


YEAR = 2021
DAY = 14

import time
from aocd import get_data, submit
from rich.console import Console

start_time = time.perf_counter()
c = Console()
data = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""

data = get_data(year=YEAR, day=DAY)
c.rule("START")


def parse(data):
    template, rules_txt = data.strip().split("\n\n")
    rules = {}
    for line in rules_txt.strip().split("\n"):
        match = re.search(r"(\w+) -> (\w+)", line)
        rules[tuple(match.group(1))] = match.group(2)
    return template, rules


template, rules = parse(data)
pairs: DefaultDict[Tuple[str, str], int] = defaultdict(int)
counts: DefaultDict[str, int] = defaultdict(int)

counts[template[0]] += 1
for i in range(1, len(template)):
    counts[template[i]] += 1
    pairs[(template[i - 1], template[i])] += 1

c.print(counts, pairs)

for i in range(40):
    new_pairs: DefaultDict[Tuple[str, str], int] = defaultdict(int)
    for key, value in pairs.items():
        insert = rules.get(key)
        if insert is None:
            new_pairs[key] += value
        else:
            new_pairs[key[0], insert] += value
            new_pairs[insert, key[1]] += value
            counts[insert] += value
    pairs = new_pairs

c.print(counts, pairs)
most_common = max(counts.values())
least_common = min(counts.values())

c.print(f"{most_common - least_common = }")
answer = most_common - least_common
c.rule(f"FINISH {time.perf_counter() - start_time}")
print(sum(counts.values()) / 1000000000000)
submit(answer, day=DAY, part="b", year=YEAR)
