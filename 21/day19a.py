from __future__ import annotations

import itertools
from dataclasses import dataclass
from functools import lru_cache
from typing import Tuple, Set


YEAR = 2021
DAY = 19

import time
from aocd import get_data
from rich.console import Console

start_time = time.perf_counter()
c = Console()
data = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
"""
data = get_data(year=YEAR, day=DAY)

c.rule("START")


@dataclass(frozen=True)
class P:
    x: int
    y: int
    z: int

    @lru_cache(maxsize=None)
    def distance(self, p: P) -> int:
        return abs(self.x - p.x) + abs(self.y - p.y) + abs(self.z - p.z)

    @lru_cache(maxsize=None)
    def r_x(self) -> P:
        return P(x=self.x, y=-self.z, z=self.y)

    @lru_cache(maxsize=None)
    def r_y(self) -> P:
        return P(x=self.z, y=self.y, z=-self.x)

    @lru_cache(maxsize=None)
    def r_z(self) -> P:
        return P(x=-self.y, y=self.x, z=self.z)

    @lru_cache(maxsize=None)
    def rotate(self, x: int = 0, y: int = 0, z: int = 0) -> P:
        # These rotations are not 'transitive'. So be careful
        # what order you do them in!
        result = self
        for i in range(z):
            result = result.r_z()
        for i in range(y):
            result = result.r_y()
        for i in range(x):
            result = result.r_x()
        return result

    @lru_cache(maxsize=None)
    def __add__(self, other) -> P:
        return P(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)

    @lru_cache(maxsize=None)
    def __sub__(self, other) -> P:
        return P(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)


def parse(data):
    scanners = []
    scanner = None
    for line in data.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("---"):
            scanner = []
            scanners.append(scanner)
            continue
        x, y, z = line.split(",")
        scanner.append(P(int(x), int(y), int(z)))
    return tuple(tuple(s) for s in scanners)


def build_all_rotations():
    orientations = [(0, 0)]  # y, z rotations
    rotations = []
    for z in (1, 3):
        orientations.append((0, z))
    for y in (1, 2, 3):
        orientations.append((y, 0))
    for x in range(4):
        for y, z in orientations:
            rotations.append((x, y, z))
    return tuple(rotations)


Data = Tuple[Tuple[P]]

# a list of lists of points.
scanners = parse(data)
all_rotations = build_all_rotations()
c.print(all_rotations)

# c.print(scanners)

origin = P(0, 0, 0)
first_beacon = scanners[0][0]
scanner_locations = set()
scanner_locations.add(P(0, 0, 0))
beacon_map: Set[P] = set(scanners[0])


def find_overlay(beacon_map, scanner):
    for candidate_beacon in beacon_map:
        remapped_beacon_map = set([b - candidate_beacon for b in beacon_map])
        for rotation in all_rotations:
            rotated_scanner = [b.rotate(*rotation) for b in scanner]
            for target_beacon in rotated_scanner:
                remapped_scanner = set(b - target_beacon for b in rotated_scanner)
                intersection = remapped_scanner.intersection(remapped_beacon_map)
                if len(intersection) >= 12:
                    c.print(f"{len(intersection) = }")
                    scanner_locations.add(candidate_beacon - target_beacon)
                    for beacon in remapped_scanner:
                        beacon_map.add(beacon + candidate_beacon)
                    c.print(f"{len(beacon_map) = }")
                    return True
    return False


scanners_to_find = set(scanners[1:])

while True:
    if not scanners_to_find:
        print("done!")
        break
    c.print(f"{len(scanners_to_find) = }")
    for scanner in scanners_to_find:
        success = find_overlay(beacon_map, scanner)
        if success:
            scanners_to_find.remove(scanner)
            break

c.print(f"{beacon_map = }")


def largest_distance(locations):
    best_distance = 0
    for a, b in itertools.permutations(locations, 2):
        distance = a.distance(b)
        if distance > best_distance:
            best_distance = distance
    return best_distance


c.print(f"{largest_distance(scanner_locations) = }")

# for every scanner, create a set representing how far every beacon is from every other beacon within that set.
# all_distances = calculate_distances(scanners)


c.rule(f"FINISH {time.perf_counter() - start_time}")
