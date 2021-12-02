from rich import print

with open("day-1-input.txt") as f:
    values = [int(i) for i in f.read().strip().split()]

from collections import deque

WS = 3
window = deque(values[:WS], maxlen=WS)
prev = sum(values[:WS])

increased = 0
for depth in values[WS:]:
    window.append(depth)
    s = sum(window)
    if s > prev:
        increased += 1
    prev = s
print(increased)
