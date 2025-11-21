#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import time
from sudokutools import generate_board

pygame.init()

class Tile:
    def __init__(self, value, window, x, y):
        self.value = value
        self.window = window
        self.rect = pygame.Rect(x, y, 60, 60)
        self.selected = False

    def draw(self):
        # Draw cell border
        pygame.draw.rect(self.window, (0, 0, 0), self.rect, 1)

        # Draw number
        if self.value != 0:
            font = pygame.font.SysFont("lato", 45)
            text = font.render(str(self.value), True, (0, 0, 0))
            self.window.blit(text, (self.rect.x + 20, self.rect.y + 10))

        # Draw selection highlight
        if self.selected:
            pygame.draw.rect(self.window, (0, 150, 255), self.rect, 3)

class Board:
    def __init__(self, window):
        self.window = window
        self.board = generate_board()
        self.tiles = [
            [Tile(self.board[r][c], window, c * 60, r * 60) for c in range(9)]
            for r in range(9)
        ]

    def draw(self, elapsed_time):
        self.window.fill((255, 255, 255))

        # Draw all tiles
        for r in range(9):
            for c in range(9):
                self.tiles[r][c].draw()

        # Draw thick grid lines
        for i in range(0, 10):
            width = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.window, (0, 0, 0), (0, i * 60), (540, i * 60), width)
            pygame.draw.line(self.window, (0, 0, 0), (i * 60, 0), (i * 60, 540), width)

        # Draw stopwatch time at bottom
        font = pygame.font.SysFont("Bahnschrift", 40)
        timer_text = font.render(elapsed_time, True, (0, 0, 0))

        # Center it below grid
        self.window.blit(timer_text, (270 - timer_text.get_width() // 2, 550))

        pygame.display.update()

    def clear_selection(self):
        for r in range(9):
            for c in range(9):
                self.tiles[r][c].selected = False

    def click(self, pos):
        x, y = pos
        if x < 540 and y < 540:
            col = x // 60
            row = y // 60
            self.clear_selection()
            self.tiles[row][col].selected = True
            return (row, col)
        return None

def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku Puzzle")

    board = Board(win)
    selected = None

    start_time = time.time()

    running = True
    while running:

        # Compute stopwatch time
        elapsed = int(time.time() - start_time)
        elapsed_h = elapsed // 3600
        elapsed_m = (elapsed % 3600) // 60
        elapsed_s = elapsed % 60

        elapsed_time_str = f"{elapsed_h:02d}:{elapsed_m:02d}:{elapsed_s:02d}"

        board.draw(elapsed_time_str)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = board.click(pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN and selected:
                r, c = selected

                if pygame.K_1 <= event.key <= pygame.K_9:
                    board.tiles[r][c].value = event.key - pygame.K_0

                if event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                    board.tiles[r][c].value = 0

    pygame.quit()

main()
