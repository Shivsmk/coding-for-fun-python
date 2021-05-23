# -*- coding: utf-8 -*-
"""
Created on Sun May 23 10:36:16 2021
@summary: 2d Terrain Generation
@author: Shiv Muthukumar
"""

import pygame
import numpy as np
import random
from statistics import mode,mean

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
            self.bucket = 0.22
        
        # ASSIGN RANDON NUMBER BETWEEN 0 AND 1 TO EACH GRID CELL
        def generateGrid(self):
            for i in range(int(self.sw/self.gs)):
                for j in range(int(self.sh/self.gs)):
                    self.grid[i][j] = random.uniform(0, 1)
        
        # COLOR CELL ACCORDING TO TERRAIN
        # WATER, SAND, GRASS, HILL, MOUNTAIN AT 0.22 INTERVALS -- LESS MOUNTAINS
        def drawGrid(self):
            for i in range(int(self.sw/self.gs)):
                for j in range(int(self.sh/self.gs)):
                    if self.grid[i][j] < self.bucket:
                        pygame.draw.rect(surface, (0, 0, 255), (i*self.gs, j*self.gs, self.gs, self.gs))
                    elif self.grid[i][j] < self.bucket*2:
                        pygame.draw.rect(surface, (194, 178, 128), (i*self.gs, j*self.gs, self.gs, self.gs))
                    elif self.grid[i][j] < self.bucket*3:
                        pygame.draw.rect(surface, (0, 255, 0), (i*self.gs, j*self.gs, self.gs, self.gs))
                    elif self.grid[i][j] < self.bucket*4:
                        pygame.draw.rect(surface, (165,42,42), (i*self.gs, j*self.gs, self.gs, self.gs))
                    else:
                        pygame.draw.rect(surface, (255, 255, 255), (i*self.gs, j*self.gs, self.gs, self.gs))
        
        # BORDERS ARE ALL WATER
        # REST GET AVERAGE OF SPECIFIC TERRAIN
        def smoothGrid(self):
            range_i = list(range(int(self.sw/self.gs)))
            range_j = list(range(int(self.sh/self.gs)))
            random.shuffle(range_i)
            random.shuffle(range_j)
            for i in range_i:
                for j in range_j:
                    if (i <= 0) or (i >= self.sw/self.gs - 1) or (j <= 0) or (j >= self.sh/self.gs - 1):
                        self.grid[i][j] = 0
                    else:
                        self.grid[i][j] = self.surroundingCells(i, j)
        
        # WITH A 9x9 GRID HAVING THE CELL IN MIDDLE
        # GET ASSIGN TERRAIN BASED ON VALUE
        # GET MOST OCCURING TERRAIN FROM ADJACENT CELLS
        # RETURN AVERAGE TERRAIN VALUE
        def surroundingCells(self, i, j):
            terrain = []
            terrain_dict = {
                "water" : [],
                "sand" : [],
                "grass" : [],
                "hill" : [],
                "mountain" : []
                }
            for k in range(i-1, i+2):
                for l in range(j-1, j+2):
                    if self.grid[k][l] < self.bucket:
                        terrain_dict["water"].append(self.grid[k][l])
                        terrain.append("water")
                    elif self.grid[k][l] < self.bucket*2:
                        terrain_dict["sand"].append(self.grid[k][l])
                        terrain.append("sand")
                    elif self.grid[k][l] < self.bucket*3:
                        terrain_dict["grass"].append(self.grid[k][l])
                        terrain.append("grass")
                    elif self.grid[k][l] < self.bucket*4:
                        terrain_dict["hill"].append(self.grid[k][l])
                        terrain.append("hill")
                    else:
                        terrain_dict["mountain"].append(self.grid[k][l])
                        terrain.append("mountain")
            return mean(terrain_dict[mode(terrain)])
    
    # CREATE A NEW GRID LAYOUT
    def newGridLayout(grid):
        grid.generateGrid()
        for i in range(5):
            grid.smoothGrid()
    
    # INITIALIZE THE GRID
    grid = Grid(gridsize, sw, sh)
    newGridLayout(grid)
    
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
                newGridLayout(grid)
        
        # GAME UPDATES
        pygame.display.update()
        clock.tick(FPS)
    
    # QUIT PYGAME
    pygame.quit()

if __name__ == "__main__":
    main()