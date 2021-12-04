from enum import Enum, auto

from rich import print
from rich.console import Console

console = Console()

console.rule("START")


class Mode(Enum):
    o2 = auto()
    co2 = auto()


# read
with open("day3a-input.txt") as f:
    input = f.read().strip().split("\n")
print(f"{input=}")


def filter_layer(input, digit, mode):
    num_ones = sum(1 for i in input if i[digit] == "1")
    num_zeros = len(input) - num_ones
    print(f"{num_ones = }, num_zeros = {num_zeros}")

    if mode is mode.o2:
        keep = "1" if num_ones >= num_zeros else "0"
    else:
        keep = "0" if num_ones >= num_zeros else "1"

    print(f"Keeping values with a {keep} in position {digit}")
    result = [value for value in input if value[digit] == keep]
    print(f"{result = }")
    return result


def filter(input, mode):
    filtered_input = input
    digit = 0
    while len(filtered_input) != 1:
        filtered_input = filter_layer(filtered_input, digit, mode)
        digit += 1
    return filtered_input[0]


console.rule("finding o2")
o2 = filter(input, Mode.o2)
console.rule("finding co2")
co2 = filter(input, Mode.co2)

console.rule("FINAL")
print(f"{o2 = }, {int(o2, base=2) = }")
print(f"{co2 = }, {int(co2, base=2) = }")
print(f"{int(o2, base=2) * int(co2, base=2) = }")
console.rule("FINISH")
