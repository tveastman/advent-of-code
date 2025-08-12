import rich.console
from aocd.models import Puzzle

c = rich.console.Console()
year = 2019
print = c.print
log = c.log

puzzle = Puzzle(year=year, day=1)
module_masses: list[int] = [int(i) for i in puzzle.input_data.split()]

total_fuel = 0
for mass in module_masses:
    fuel = (mass // 3) - 2
    total_fuel += fuel

puzzle.answer_a = total_fuel
log(f"{puzzle.answer_a=}")


def recursive_fuel(fuel: int) -> int:
    required = (fuel // 3) - 2
    if required <= 0:
        return 0
    else:
        return required + recursive_fuel(required)


answer_b = sum(recursive_fuel(mass) for mass in module_masses)

puzzle.answer_b = answer_b
log(f"{puzzle.answer_b=}")
