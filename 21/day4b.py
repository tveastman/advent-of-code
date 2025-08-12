# started at 7.30pmish
from typing import List

from more_itertools import chunked
from rich.console import Console

c = Console()


class BingoBoard:
    id_seq = 0

    def __init__(self, board: List[int]):
        self.id = BingoBoard.id_seq
        BingoBoard.id_seq += 1
        self.board = board
        self.sum_unmarked = sum(board)
        self.cols = [0] * 5
        self.rows = [0] * 5
        self.finished = False

    def mark(self, number):
        if self.finished:
            return
        try:
            ix = self.board.index(number)
        except ValueError:
            return
        self.sum_unmarked -= number
        self.rows[ix // 5] += 1
        self.cols[ix % 5] += 1
        if 5 in self.rows or 5 in self.cols:
            self.finished = True
            final_score = number * self.sum_unmarked
            c.print(f"Bingo! {board.id=} {final_score = }")


with open("day4-input.txt") as f:
    draws = [int(i) for i in f.readline().strip().split(",")]
    boards = [
        BingoBoard(i) for i in (chunked((int(i) for i in f.read().strip().split()), 25))
    ]

c.rule("START")
for number in draws:
    for board in boards:
        board.mark(number)
