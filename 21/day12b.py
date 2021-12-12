from collections import defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from itertools import combinations, product, permutations, combinations_with_replacement
from typing import Tuple, Set, List, Dict, DefaultDict, Optional, FrozenSet

from more_itertools import chunked

YEAR = 2021
DAY = 12

import time
from aocd import get_data, submit
from rich.console import Console

start_time = time.perf_counter()
c = Console()
data = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""


data = get_data(year=YEAR, day=DAY)
c.rule("START")

paths: DefaultDict[str, Set[str]] = defaultdict(set)
for line in data.strip().split("\n"):
    a, b = line.strip().split("-")
    paths[a].add(b)
    paths[b].add(a)


@lru_cache(maxsize=0)
def find_paths(
    current_location: str,
    destination: str,
    blocklist: Optional[FrozenSet] = None,
    path_so_far: Optional[Tuple[str]] = None,
    completed_paths: Optional[FrozenSet[Tuple[str]]] = None,
    visit_twice: str = "",
):
    if blocklist is None:
        blocklist = frozenset()
    if path_so_far is None:
        path_so_far = tuple()
    if completed_paths is None:
        completed_paths = frozenset()
    path_so_far = path_so_far + (current_location,)
    # c.print(visit_twice, path_so_far)
    if current_location.islower() and current_location != visit_twice:
        blocklist = blocklist.union({current_location})
    if current_location == visit_twice:
        visit_twice = ""
    if current_location == destination:
        # c.print(f"NEW COMPLETE PATH {path_so_far = }")
        completed_paths = completed_paths.union(frozenset([path_so_far]))
    else:
        for connection in paths[current_location]:
            if connection not in blocklist:
                result = find_paths(
                    connection,
                    destination,
                    blocklist,
                    path_so_far,
                    completed_paths,
                    visit_twice,
                )
                completed_paths = completed_paths.union(result)
    return completed_paths
    pass


small_caves = [i for i in paths.keys() if i.islower() and i != "start" and i != "end"]
c.print("Small Caves:", small_caves)

all_paths = frozenset()
for small_cave in small_caves:
    all_paths = all_paths.union(
        find_paths(current_location="start", destination="end", visit_twice=small_cave)
    )
    print(f"{small_cave = }, {len(all_paths) = }")
    # break

c.rule(f"FINISH {time.perf_counter() - start_time}")

answer = len(all_paths)
print(f"{answer = }")
# submit(answer, day=DAY, part="a", year=YEAR)
