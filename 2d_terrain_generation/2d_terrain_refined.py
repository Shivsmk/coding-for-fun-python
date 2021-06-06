# -*- coding: utf-8 -*-
"""
Created on Sun May 23 10:36:16 2021
@summary: 2d Terrain Generation using perlin noise library
@author: Shiv Muthukumar
"""

import pygame
from perlin_noise import PerlinNoise

def main():
    # CONSTANTS
    sh = 700
    sw = 700
    FPS = 50
    
    # PARAMETERS
    gridsize = 2
    
    # INITIALIZATION
    pygame.init()
    surface = pygame.display.set_mode((sh, sw))
    clock = pygame.time.Clock()
    
    # CLASS DECLARATION
    class Grid():
        def __init__(self, gs, sw, sh):
            self.gs = gs
            self.sh = sh
            self.sw = sw
            self.x_iter = int(self.sw/self.gs)
            self.y_iter = int(self.sh/self.gs)
        
        # ASSIGN RANDON NUMBER BETWEEN 0 AND 1 TO EACH GRID CELL
        def generateGrid(self):
            self.grid = []
            noise1 = PerlinNoise(octaves=3)
            noise2 = PerlinNoise(octaves=6)
            noise3 = PerlinNoise(octaves=12)
            noise4 = PerlinNoise(octaves=24)
            for i in range(self.x_iter):
                row = []
                for j in range(self.y_iter):
                    noise_val =         noise1([i/self.x_iter, j/self.y_iter])
                    noise_val += 0.5  * noise2([i/self.x_iter, j/self.y_iter])
                    noise_val += 0.25 * noise3([i/self.x_iter, j/self.y_iter])
                    noise_val += 0.125* noise4([i/self.x_iter, j/self.y_iter])
                    row.append(noise_val)
                self.grid.append(row)
        
        def paint_terrain(self, i, j):
            if self.grid[i][j] <= 0.0:
                color_code = (0,100,200)
            elif self.grid[i][j] <= 0.1:
                color_code = (200,150,100)
            elif self.grid[i][j] <= 0.4:
                color_code = (130,240,0)
            elif self.grid[i][j] <= 0.7:
                color_code = (100,60,20)
            else:
                color_code = (255, 240, 240)
            pygame.draw.rect(surface, color_code, (i*self.gs, j*self.gs, self.gs, self.gs))
            
        
        def drawGrid(self):
            for i in range(self.x_iter):
                for j in range(self.y_iter):
                    self.paint_terrain(i, j)
        
    def newGridLayout(grid):
        grid.generateGrid()
        grid.drawGrid()
    
    # INITIALIZE AND DRAW THE GRID
    grid = Grid(gridsize, sw, sh)
    newGridLayout(grid)
    
    # GAME LOOP
    while True:
        # EXIT GAME LOOP ON SCREEN CLOSE
        if pygame.event.peek(pygame.QUIT):
            break

        # GENERATE NEW GRID ON MOUSE CLICK
        for event in pygame.event.get():    
            if event.type == pygame.MOUSEBUTTONDOWN :
                newGridLayout(grid)
        
        # GAME UPDATES
        pygame.display.update()
        clock.tick(FPS)
    
    # QUIT PYGAME
    pygame.quit()

if __name__ == "__main__":
    main()