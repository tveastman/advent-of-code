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


def multiply_map(nodes, multiplier):
    len_x = max(p.x for p in nodes) + 1
    len_y = max(p.y for p in nodes) + 1
    new_nodes = {}
    for x in range(multiplier):
        for y in range(multiplier):
            if x == 0 and y == 0:
                new_nodes.update(nodes)
            else:
                for node in nodes.values():
                    p = Point(x=node.p.x + (len_x * x), y=node.p.y + (len_y * y))
                    r = node.r + (x + y)
                    while r > 9:
                        r -= 9
                    new_nodes[p] = Node(p, r)

    return (
        new_nodes,
        new_nodes[Point((len_x * multiplier) - 1, (len_y * multiplier) - 1)],
    )


nodes, _ = parse(data)

nodes, end = multiply_map(nodes, 5)

# sys.exit()
# c.print(nodes, end)

g = build_graph(nodes)
# c.print(g)

start = nodes[Point(0, 0)]

start_time = time.perf_counter()
sp = shortest_path(g, start, end, weight="r")
# c.print(sp)

cost_of_shortest_path = sum(node.r for node in sp[1:])
c.print(f"{cost_of_shortest_path = }")
c.rule(f"FINISH {time.perf_counter() - start_time}")


def print_path(nodes, sp):
    sp = set(sp)
    max_x = max(p.x for p in nodes)
    max_y = max(p.y for p in nodes)

    for y in range(max_y + 1):
        line = []
        for x in range(max_x + 1):
            n = nodes[Point(x, y)]
            if n in sp:
                line.append(f"[bold yellow]{str(n.r)}[/]")
            else:
                line.append(str(n.r))
        c.print("".join(line))


# print_path(nodes, sp)
