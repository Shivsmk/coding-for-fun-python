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
    gridsize = 5
    
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
            self.grid = []
            self.x_iter = int(self.sw/self.gs)
            self.y_iter = int(self.sh/self.gs)
        
        # ASSIGN RANDON NUMBER BETWEEN 0 AND 1 TO EACH GRID CELL
        def generateGrid(self):
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
            
        def drawGrid(self):
            for i in range(self.x_iter):
                for j in range(self.y_iter):
                    color_code = 255*(self.grid[i][j]+1)/2
                    pygame.draw.rect(surface, (color_code, color_code, color_code), (i*self.gs, j*self.gs, self.gs, self.gs))
        
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