from rich import print

with open("day-1-input.txt") as f:
    values = [int(i) for i in f.read().strip().split()]


def increases(a, b):
    return a is not None and a < b


result = 0
for i in range(1, len(values)):
    if increases(values[i - 1], values[i]):
        result += 1

print(result)
