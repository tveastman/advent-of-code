import rich.console
from aocd.models import Puzzle
from collections import defaultdict

YEAR = 2015
DAY = 5

c = rich.console.Console()
print = c.print
log = c.log
puzzle = Puzzle(year=YEAR, day=DAY)
c.rule(f"{puzzle.title} ({YEAR}-{DAY})")

strings = puzzle.input_data.split()


def is_nice(s: str) -> bool:
    vowels = 0
    twice = False
    for i, char in enumerate(s):
        if char in "aeiou":
            vowels += 1
        if i > 0:
            pair = s[i - 1] + char
            if pair[0] == pair[1]:
                twice = True
            if pair in ["ab", "cd", "pq", "xy"]:
                return False
    return vowels >= 3 and twice


log(f"{is_nice('ugknbfddgicrmopn')=}")
log(f"{is_nice('aaa')=}")
log(f"{is_nice('jchzalrnumimnmhp')=}")
log(f"{is_nice('haegwjzuvuyypxyu')=}")
log(f"{is_nice('dvszwmarrgswjxmb')=}")

nice_strings_count = 0
for s in strings:
    if is_nice(s):
        nice_strings_count += 1

print(f"{nice_strings_count=}")
puzzle.answer_a = nice_strings_count


def has_two_pairs(s: str) -> True:
    for i in range(2, len(s)):
        pair = s[i - 2] + s[i - 1]
        if pair in s[i:]:
            log(f"Found pair {pair}")
            return True
    return False


def has_sandwitch(s):
    for i in range(2, len(s)):
        first = s[i - 2]
        second = s[i - 1]
        third = s[i]
        #        log(first, second, third)
        if first == third and first != second:
            return True
    return False


def is_nice(s: str) -> bool:
    return has_two_pairs(s) and has_sandwitch(s)


print(f"{is_nice('qjhvhtzxzqqjkmpb')=}")
print(f"{is_nice('xxyxx')=}")
print(f"{is_nice('uurcxstgmygtbstg')=}")
print(f"{is_nice('ieodomkazucvgmuy')=}")

nice_strings_count = 0
for s in strings:
    if is_nice(s):
        nice_strings_count += 1

print(f"{nice_strings_count=}")
puzzle.answer_b = nice_strings_count
