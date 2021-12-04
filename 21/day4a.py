# started at 7pmish
import sys
from typing import List

from more_itertools import chunked
from rich.console import Console

c = Console()


class BingoBoard:
    def __init__(self, board: List[int]):
        self.board = board
        self.sum_unmarked = sum(board)
        self.cols = [0] * 5
        self.rows = [0] * 5

    def mark(self, number):
        try:
            ix = self.board.index(number)
        except ValueError:
            return
        self.sum_unmarked -= number
        self.rows[ix // 5] += 1
        self.cols[ix % 5] += 1
        if 5 in self.rows or 5 in self.cols:
            return number * self.sum_unmarked


with open("day4-input.txt") as f:
    draws = [int(i) for i in f.readline().strip().split(",")]
    boards = [
        BingoBoard(i) for i in (chunked((int(i) for i in f.read().strip().split()), 25))
    ]


for number in draws:
    for board in boards:
        winner = board.mark(number)
        if winner is not None:
            c.print(f"{winner = }")
            sys.exit()
