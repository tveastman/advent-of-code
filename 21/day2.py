from rich import print

with open("input-day2.txt") as f:
    lines = f.read().strip().split("\n")

# lines = lines[:30]

horizontal = 0
depth = 0
for line in lines:
    command, value = line.split()
    value = int(value)

    if command == "forward":
        horizontal += value
    elif command == "up":
        depth -= value
    elif command == "down":
        depth += value

    print(f"{line=}, {horizontal=}, {depth=}, {horizontal*depth=}")
