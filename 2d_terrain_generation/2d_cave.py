# -*- coding: utf-8 -*-
"""
Created on Sun May 23 10:36:16 2021
@summary: 2d Terrain Generation
@author: Shiv Muthukumar
"""

import pygame
import numpy as np
import random

def main():
    # CONSTANTS
    sh = 700
    sw = 700
    FPS = 50
    
    # PARAMETERS
    gridsize = 10
    
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
            self.grid = np.zeros((int(self.sw/self.gs), int(self.sh/self.gs)))
        
        # ASSIGN RANDON NUMBER BETWEEN 0 AND 1 TO EACH GRID CELL
        def generateGrid(self):
            for i in range(int(self.sw/self.gs)):
                for j in range(int(self.sh/self.gs)):
                    self.grid[i][j] = random.uniform(0, 1)
        
        # COLOR CELL BLACK IF RANDON NUMBER > 0.5
        def drawGrid(self):
            for i in range(int(self.sw/self.gs)):
                for j in range(int(self.sh/self.gs)):
                    if self.grid[i][j] >= 0.5:
                        pygame.draw.rect(surface, (0, 0, 0), (i*self.gs, j*self.gs, self.gs, self.gs))
        
        # IF COUNT OF BLACK CELLS SURROUNDING A CELL > 4 (MAX 8), COLOR BLACK
        # ELSE COLOR WHITE
        def smoothGrid(self):
            for i in range(int(self.sw/self.gs)):
                for j in range(int(self.sh/self.gs)):
                    if (i <= 0) or (i >= self.sw/self.gs - 1) or (j <= 0) or (j >= self.sh/self.gs - 1):
                        self.grid[i][j] = 1
                    elif self.countSurroundingCells(i, j) > 4.5 :
                        self.grid[i][j] = 1
                    elif self.countSurroundingCells(i, j) < 2.5 :
                        self.grid[i][j] = 0
        
        def countSurroundingCells(self, i, j):
            countCells = 0
            for k in range(i-1, i+2):
                for l in range(j-1, j+2):
                    if not ((i == k) and (j == l)):
                        if self.grid[k][l] > 0.5:
                            countCells += self.grid[k][l]
            return countCells
    
    # CREATE A NEW GRID LAYOUT
    def newGridLayout():
        # OBJECT CREATION
        grid = Grid(gridsize, sw, sh)
        grid.generateGrid()
        for i in range(5):
            grid.smoothGrid()
        return grid
    
    # INITIALIZE THE GRID
    grid=newGridLayout()
    
    # GAME LOOP
    while True:
        # EXIT GAME LOOP ON SCREEN CLOSE
        if pygame.event.peek(pygame.QUIT):
            break
        
        # SIMULATION MAGIC
        surface.fill((255, 255, 255))
        
        # DRAW GRID
        grid.drawGrid()
        
        # GENERATE NEW GRID ON MOUSE CLICK
        for event in pygame.event.get():    
            if event.type == pygame.MOUSEBUTTONDOWN :
                grid=newGridLayout()
        
        # GAME UPDATES
        pygame.display.update()
        clock.tick(FPS)
    
    # QUIT PYGAME
    pygame.quit()

if __name__ == "__main__":
    main()