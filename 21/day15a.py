from dataclasses import dataclass
from typing import List, Dict

import networkx as nx
from networkx import shortest_path

YEAR = 2021
DAY = 15

import time
from aocd import get_data
from rich.console import Console

start_time = time.perf_counter()
c = Console()

data = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""
data = get_data(year=YEAR, day=DAY)
c.rule("START")


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Node:
    p: Point
    r: int


def neighbours(nodes: Dict[Point, Node], point: Point) -> List[Node]:
    result = []
    for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        if dx == 0 and dy == 0:
            continue
        n = nodes.get(Point(x=point.x + dx, y=point.y + dy))
        if n is not None:
            result.append(n)
    return result


def parse(data):
    nodes = {}
    max_x = 0
    max_y = 0
    for y, line in enumerate(data.strip().split()):
        max_y = max(y, max_y)
        for x, char in enumerate(line.strip()):
            max_x = max(x, max_x)
            n = Node(p=Point(x=int(x), y=int(y)), r=int(char))
            nodes[n.p] = n
    return nodes, nodes[Point(max_x, max_y)]


def build_graph(nodes):
    g = nx.DiGraph()
    for point, node in nodes.items():
        for neighbour in neighbours(nodes, point):
            g.add_edge(node, neighbour, r=neighbour.r)
    return g


nodes, end = parse(data)
g = build_graph(nodes)
c.print(g)

# c.print(len(nodes))
# for item in nodes.items():
#    c.print(neighbours(nodes, item[0]))
start = nodes[Point(0, 0)]
sp = shortest_path(g, start, end, weight="r", method="bellman-ford")
c.print(sp)

cost_of_shortest_path = sum(node.r for node in sp[1:])
c.print(f"{cost_of_shortest_path = }")

c.rule(f"FINISH {time.perf_counter() - start_time}")
