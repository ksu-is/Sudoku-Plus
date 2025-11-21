#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import time
from sudokutools import generate_board, solve

pygame.init()

class Tile:
    def __init__(self, value, window, x, y, locked):
        self.value = value
        self.window = window
        self.rect = pygame.Rect(x, y, 60, 60)
        self.selected = False
        self.locked = locked

    def draw(self, correct):
        # Gray background for correct tiles
        if correct:
            pygame.draw.rect(self.window, (210, 210, 210), self.rect)

        # Border
        pygame.draw.rect(self.window, (0, 0, 0), self.rect, 1)

        # Number
        if self.value != 0:
            font = pygame.font.SysFont("lato", 45)
            text = font.render(str(self.value), True, (0, 0, 0))
            self.window.blit(text, (self.rect.x + 20, self.rect.y + 10))

        # Blue highlight if selected
        if self.selected and not self.locked:
            pygame.draw.rect(self.window, (0, 150, 255), self.rect, 3)


class Board:
    def __init__(self, window):
        self.window = window

        # Generate puzzle
        self.board = generate_board()

        # Solve puzzle
        self.solution = [row[:] for row in self.board]
        solve(self.solution)

        # Build tiles
        self.tiles = []
        for r in range(9):
            row_tiles = []
            for c in range(9):
                locked = (self.board[r][c] != 0)
                row_tiles.append(Tile(self.board[r][c], window, c * 60, r * 60, locked))
            self.tiles.append(row_tiles)

    def draw(self, elapsed_time):
        self.window.fill((255, 255, 255))

        # Draw tiles
        for r in range(9):
            for c in range(9):
                correct = (self.tiles[r][c].value == self.solution[r][c] and self.tiles[r][c].value != 0)
                self.tiles[r][c].draw(correct)

        # Thick 3x3 grid lines
        for i in range(10):
            width = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.window, (0, 0, 0), (0, i * 60), (540, i * 60), width)
            pygame.draw.line(self.window, (0, 0, 0), (i * 60, 0), (i * 60, 540), width)

        # =========================
        # FIXED TIMER BOXES
        # =========================

        font = pygame.font.SysFont("Bahnschrift", 40)
        mm = elapsed_time[0:2]
        ss = elapsed_time[3:5]
        ms = elapsed_time[6:8]

        min_text = font.render(mm, True, (0, 0, 0))
        sec_text = font.render(ss, True, (0, 0, 0))
        ms_text  = font.render(ms, True, (0, 0, 0))

        min_x, sec_x, ms_x = 160, 260, 360
        box_y = 550

        pygame.draw.rect(self.window, (230, 230, 230), (min_x, box_y, 60, 45))
        pygame.draw.rect(self.window, (230, 230, 230), (sec_x, box_y, 60, 45))
        pygame.draw.rect(self.window, (230, 230, 230), (ms_x,  box_y, 60, 45))

        self.window.blit(min_text, (min_x + 12, box_y + 5))
        self.window.blit(sec_text, (sec_x + 12, box_y + 5))
        self.window.blit(ms_text,  (ms_x  + 12, box_y + 5))

        colon = font.render(":", True, (0, 0, 0))
        self.window.blit(colon, (min_x + 60, box_y + 5))
        self.window.blit(colon, (sec_x + 60, box_y + 5))

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

            if self.tiles[row][col].locked:
                return None

            self.clear_selection()
            self.tiles[row][col].selected = True
            return (row, col)

        return None

    # =============================
    #     ARROW KEY MOVEMENT
    # =============================
    def move_selection(self, current, key):
        if not current:
            return None  # No tile selected yet

        r, c = current

        if key == pygame.K_UP:
            r = (r - 1) % 9
        elif key == pygame.K_DOWN:
            r = (r + 1) % 9
        elif key == pygame.K_LEFT:
            c = (c - 1) % 9
        elif key == pygame.K_RIGHT:
            c = (c + 1) % 9

        # Skip locked tiles
        while self.tiles[r][c].locked:
            if key == pygame.K_UP:
                r = (r - 1) % 9
            elif key == pygame.K_DOWN:
                r = (r + 1) % 9
            elif key == pygame.K_LEFT:
                c = (c - 1) % 9
            elif key == pygame.K_RIGHT:
                c = (c + 1) % 9

        self.clear_selection()
        self.tiles[r][c].selected = True
        return (r, c)


def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku Puzzle")

    board = Board(win)
    selected = None

    start_time = time.time()
    penalty = 0

    running = True
    while running:
        elapsed = (time.time() - start_time + penalty)
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        milliseconds = int((elapsed * 100) % 100)
        elapsed_str = f"{minutes:02d}:{seconds:02d}:{milliseconds:02d}"

        board.draw(elapsed_str)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mouse selection
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = board.click(pygame.mouse.get_pos())

            # Keyboard input
            if event.type == pygame.KEYDOWN:

                # Arrow keys → move selection
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    selected = board.move_selection(selected, event.key)

                # No tile selected? skip
                if not selected:
                    continue

                r, c = selected

                if board.tiles[r][c].locked:
                    continue

                # Number keys
                if pygame.K_1 <= event.key <= pygame.K_9:
                    val = event.key - pygame.K_0

                    if val != board.solution[r][c]:
                        penalty += 5
                    else:
                        board.tiles[r][c].value = val

                # Clear
                if event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                    board.tiles[r][c].value = 0

    pygame.quit()


main()
