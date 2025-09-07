import typing

import attrs
import re
import rich.console
from aocd.models import Puzzle
import array
import itertools

YEAR = 2015
DAY = 19

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")


def findall(string, sub):
    results: list[int] = []
    start = 0
    while True:
        result = string.find(sub, start)
        if result == -1:
            break
        else:
            results.append(result)
            start = result + 1
    return results


def splice(string, i, n, sub):
    prefix = string[:i]
    suffix = string[i + n :]
    return prefix + sub + suffix


def spliceall(string, input, replacement):
    results: set[str] = set()
    for i in findall(string, input):
        result = splice(string, i, len(input), replacement)
        results.add(result)
    return results


pairs_input, calibration_molecule = puzzle.input_data.split("\n\n")
calibration_molecule = calibration_molecule.strip()

pairs = []
for line in pairs_input.splitlines():
    input, replacement = line.split(" => ")
    pairs.append((input.strip(), replacement.strip()))

molecules = set()
for input, replacement in pairs:
    molecules.update(spliceall(calibration_molecule, input, replacement))

puzzle.answer_a = len(molecules)


input = """e => H
e => O
H => HO
H => OH
O => HH

HOHOHO"""

input = puzzle.input_data

pairs_input, calibration_molecule = input.split("\n\n")
calibration_molecule = calibration_molecule.strip()

pairs = []
for line in pairs_input.splitlines():
    input, replacement = line.split(" => ")
    pairs.append((input.strip(), replacement.strip()))


print(pairs)
pairs = [(b, a) for (a, b) in pairs]
pairs.sort(key=lambda a: -len(a[0]))
print(pairs)
searched = set()


def dfs(molecule, step=0):
    print(molecule)
    if molecule == "e":
        print(f"Found it! {step=}")
        return step
    all_possible_next_steps = set()
    for input, replacement in pairs:
        all_possible_next_steps.update(spliceall(molecule, input, replacement))
    next_molecules = sorted(all_possible_next_steps, key=lambda x: len(x))
    for n in next_molecules:
        result = dfs(n, step + 1)
        if step is not None:
            return result


result = dfs(calibration_molecule)
print(result)
puzzle.answer_b = result
