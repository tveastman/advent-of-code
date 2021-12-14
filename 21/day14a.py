from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
import re
from typing import Any, Optional

from more_itertools import chunked

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


@dataclass()
class Node:
    data: Optional[str] = None
    next: Optional[Node] = None

    def insert_after(self, data: str) -> Node:
        n = Node(data=data)
        n.next = self.next
        self.next = n
        return n

    def list(self):
        result = []
        n = self
        while n is not None:
            result.append(n.data)
            n = n.next
        return result

    def rules_insert(self, rules):
        n = self
        while n.next is not None:
            c1, c2 = n.data, n.next.data
            rule = rules.get((c1, c2))
            if rule:
                next = n.next
                new = n.insert_after(rule)
                n = next
            else:
                n = n.next


def parse(data):
    template, rules_txt = data.strip().split("\n\n")
    rules = {}
    for line in rules_txt.strip().split("\n"):
        match = re.search(r"(\w+) -> (\w+)", line)
        rules[tuple(match.group(1))] = match.group(2)
    return template, rules


template, rules = parse(data)
head = Node(data=template[0])
cursor = head
for char in template[1:]:
    cursor = cursor.insert_after(char)

for iteration in range(10):
    # c.print("".join(head.list()))
    head.rules_insert(rules)

counts = defaultdict(int)
for item in head.list():
    counts[item] += 1
most_common = max(counts.items(), key=lambda x: x[1])
least_common = min(counts.items(), key=lambda x: x[1])
c.print(most_common, least_common)
c.print(f"{most_common[1] - least_common[1]}")
answer_a = most_common[1] - least_common[1]
print(counts)

c.rule(f"FINISH {time.perf_counter() - start_time}")

# print(f"{answer = }")
submit(answer_a, day=DAY, part="a", year=YEAR)
