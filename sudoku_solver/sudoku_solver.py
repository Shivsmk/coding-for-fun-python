# -*- coding: utf-8 -*-

from dataclasses import dataclass
from math import floor
from os import getcwd, path

import numpy as np


@dataclass
class Sudoku:
    input_file: str

    def __post_init__(self):
        # SETUP SUDOKU BOARD WITH 0 BEING EMPTY
        self.board: np.ndarray = np.zeros((9, 9))

        # READ BOARD FROM FILE
        __location__ = path.realpath(path.join(getcwd(), path.dirname(__file__)))
        with open(path.join(__location__, self.input_file), encoding="utf8") as file:
            row = 0
            for line in file:
                line = line.strip()
                col = 0
                for i in line:
                    self.board[row][col] = int(i)
                    col += 1
                row += 1

        # A SET OF ALL NUMBERS 1-9 (INCLUSIVE)
        self.set = set(range(1, 10))

    # FIND ALLOWED NUMBERS BASED ON THE CORRESPONDING 3X3 SUDOKU SUB-GRID
    # THAT THE GIVEN CELL IS A PART OFF
    def square_find(self, row: int, col: int) -> set:
        x_off = 3 * floor(row / 3)
        y_off = 3 * floor(col / 3)
        square_set = set()
        for i in range(3):
            for j in range(3):
                if self.board[i + x_off][j + y_off] != 0:
                    square_set.add(self.board[i + x_off][j + y_off])
        return self.set - square_set

    # FIND ALLOWED NUMBERS BASED ON THE CELL'S ROW
    def row_find(self, row: int) -> set:
        row_set = set()
        for i in range(9):
            if self.board[row][i] != 0:
                row_set.add(self.board[row][i])
        return self.set - row_set

    # FIND ALLOWED NUMBERS BASED ON THE CELL'S COLUMN
    def col_find(self, col: int) -> set:
        col_set = set()
        for i in range(9):
            if self.board[i][col] != 0:
                col_set.add(self.board[i][col])
        return self.set - col_set

    # FIND ALL THE ALLOWED NUMBERS GIVEN A CELL
    def get_allowed_numbers(self, row: int, col: int) -> list:
        return list(
            set.intersection(
                self.square_find(row=row, col=col),
                self.row_find(row=row),
                self.col_find(col=col),
            )
        )

    # SOLVE BY FINDING AND FILLLING ALL THE CELLS
    # THAT CAN ONLY TAKE 1 POSSIBLE NUMBER
    # DUE TO THE CONSTRAINTS PROVIDED
    def solver_distinct(self) -> None:
        solve: bool = True
        while solve:
            has_change: bool = False
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] == 0:
                        allowed_numbers = self.get_allowed_numbers(row=i, col=j)
                        if len(allowed_numbers) == 1:
                            self.board[i][j] = allowed_numbers[0]
                            has_change = True
            if not has_change:
                solve = False

    # SOLVE BY FINDING AND FILLING CELLS
    # IN A 3X3 GRID BY ELIMINATING THE ALLOWED NUMBERS
    # TILL ONLY 1 NUMBER IS POSSIBLE FOR THE CELL
    def solver_eliminate(self) -> None:
        solve: bool = True
        while solve:
            has_change: bool = False
            for i in [0, 3, 6]:
                for j in [0, 3, 6]:
                    square: dict = {}
                    for m in range(3):
                        for n in range(3):
                            if self.board[i + m][j + n] == 0:
                                square[
                                    str(i + m) + str(j + n)
                                ] = self.get_allowed_numbers(row=i + m, col=j + n)
                    if square.keys():
                        for a_key, a_value in square.items():
                            square_2: dict = square.copy()
                            del square_2[a_key]
                            a_set = set(a_value)
                            for b_value in square_2.values():
                                a_set = a_set - set(b_value)
                            if len(list(a_set)) == 1:
                                self.board[int(a_key[0])][int(a_key[1])] = list(a_set)[
                                    0
                                ]
                                has_change = True
            if not has_change:
                solve = False

    # PERFORM THE OVERALL SOLVE.
    def solve(self, brute: bool = False) -> None:
        for _ in range(3):
            self.solver_distinct()
            self.solver_eliminate()
        if brute:
            self.solve_brute()

    # CHECKS IF THE SUDOKU BOARD IS FILLED UP COMPLETELY
    def check_complete(self) -> bool:
        if np.count_nonzero(self.board) == 81:
            return True
        else:
            return False

    # SOLVES BY GOING THROUGH THE ALLOWED NUMBERS FOR A CELL
    # AND SOLVING BY DISTINCT AND ELIMINATE FUNCTION
    # TILL A COMPLETE BOARD IS FOUND - WHICH IS THE SOLUTION
    def solve_brute(self) -> None:
        backup_board: np.ndarray = np.copy(self.board)
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    allowed_numbers: list = self.get_allowed_numbers(row=i, col=j)
                    for num in allowed_numbers:
                        self.board[i][j] = num
                        self.solve(brute=False)
                        if self.check_complete():
                            return
                        else:
                            self.board = np.copy(backup_board)


def main():
    S = Sudoku("evil.txt")
    print("Before:")
    print(S.board)
    print("After:")
    S.solve(brute=True)
    print(S.board)


if __name__ == "__main__":
    main()
