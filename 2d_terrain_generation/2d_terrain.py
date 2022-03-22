# -*- coding: utf-8 -*-
"""
Created on Sun May 23 10:36:16 2021
Modified on Tue Mar 22 09:48:00 2022
@summary: 2d Terrain Generation using noise library
@author: Shiv Muthukumar
"""

from random import randint

import numpy as np
import pygame
from noise import snoise2


def main():
    # CONSTANTS
    sh = 500
    sw = 500
    FPS = 50

    # PARAMETERS
    gridsize = 1

    # INITIALIZATION
    pygame.init()
    surface = pygame.display.set_mode((sw, sh))
    clock = pygame.time.Clock()

    # CLASS DECLARATION
    class Grid:
        def __init__(self, gs, sw, sh):
            self.gs = gs
            self.sh = sh
            self.sw = sw
            self.x_iter = int(self.sw / self.gs)
            self.y_iter = int(self.sh / self.gs)

        # ASSIGN RANDON NUMBER BETWEEN 0 AND 1 TO EACH GRID CELL
        def generate_grid(self):
            self.grid = []
            seed = randint(0, 4096)
            freq = randint(100, 300)
            for i in range(self.x_iter):
                row = []
                for j in range(self.y_iter):
                    val = (
                        snoise2(i / freq, j / freq, octaves=3, base=seed)
                        + 0.5 * snoise2(i / freq, j / freq, octaves=6, base=seed)
                        + 0.25 * snoise2(i / freq, j / freq, octaves=12, base=seed)
                        + 0.125 * snoise2(i / freq, j / freq, octaves=24, base=seed)
                    )
                    row.append(val)
                self.grid.append(row)

        def paint_terrain(self, i, j):
            if self.grid[i][j] <= 0.0:
                color_code = (0, 100, 200)
            elif self.grid[i][j] <= 0.1:
                color_code = (200, 150, 100)
            elif self.grid[i][j] <= 0.5:
                color_code = (130, 240, 0)
            elif self.grid[i][j] <= 0.8:
                color_code = (100, 60, 20)
            else:
                color_code = (255, 240, 240)
            return color_code
            # pygame.draw.rect(surface, color_code, (i*self.gs, j*self.gs, self.gs, self.gs))

        def draw_grid(self, pixelArray):
            for i in range(self.x_iter):
                for j in range(self.y_iter):
                    pixelArray[i][j] = self.paint_terrain(i, j)

    def new_grid_layout(grid):
        grid.generate_grid()
        pixelArray = pygame.PixelArray(surface)
        grid.draw_grid(pixelArray)

    # INITIALIZE AND DRAW THE GRID
    grid = Grid(gridsize, sw, sh)
    new_grid_layout(grid)

    # GAME LOOP
    while True:
        # EXIT GAME LOOP ON SCREEN CLOSE
        if pygame.event.peek(pygame.QUIT):
            break

        # GENERATE NEW GRID ON MOUSE CLICK
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                new_grid_layout(grid)

        # GAME UPDATES
        pygame.display.update()
        clock.tick(FPS)

    # QUIT PYGAME
    pygame.quit()


if __name__ == "__main__":
    main()
