#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint, shuffle

def valid(board, pos, num):
    # Check row
    for j in range(9):
        if board[pos[0]][j] == num:
            return False

    # Check column
    for i in range(9):
        if board[i][pos[1]] == num:
            return False

    # Check 3×3 box
    box_i = pos[0] - pos[0] % 3
    box_j = pos[1] - pos[1] % 3
    for i in range(3):
        for j in range(3):
            if board[box_i + i][box_j + j] == num:
                return False

    return True

def solve(board):
    empty = None
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                empty = (i, j)
                break
        if empty:
            break

    if not empty:
        return True

    r, c = empty
    for num in range(1, 10):
        if valid(board, (r, c), num):
            board[r][c] = num
            if solve(board):
                return True
            board[r][c] = 0

    return False

def generate_board():
    """Generate a valid Sudoku puzzle."""
    board = [[0 for _ in range(9)] for _ in range(9)]

    # Fill diagonal boxes
    for i in range(0, 9, 3):
        nums = list(range(1, 10))
        shuffle(nums)
        for r in range(3):
            for c in range(3):
                board[i + r][i + c] = nums.pop()

    # Solve to get a full valid solution
    solve(board)

    # Remove numbers to create puzzle
    for _ in range(randint(55, 65)):
        i, j = randint(0, 8), randint(0, 8)
        board[i][j] = 0

    return board
