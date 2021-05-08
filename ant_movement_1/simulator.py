# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 18:23:11 2021
@summary: Basic Ant movement engine. Move radom, avoid walls, avoid each other.
@author: Shiv SMK
"""

import pygame
import engine

def main():
    # INITIALIZE PYGAME
    pygame.init()
    
    # CONSTANTS
    sh = 600
    sw = 600
    FPS = 60
    motivation = 0.1
    fov_th = 90
    
    # PARAMETERS
    population = 1000
    find_knn = False
    
    # SET SURFACE
    surface = pygame.display.set_mode((sh, sw))
        
    # INITIALIZE ANTS
    pos_arr,theta_arr,color_arr,KNN_arr = engine.initAnts(population, sh, sw)
    
    while True:
        
        # EXIT GAME LOOP ON SCREEN CLOSE
        if pygame.event.peek(pygame.QUIT):
            break
        
        # RESET SCREEN
        surface.fill((255, 255, 255))
        
        # DRAW
        # IF FIND_KNN = TRUE
        # DRAW OBJECT 0 AS RED AND ITS NEAREST NEIGHBOUR AS BLUE FOR TRACKING
        # ELSE DRAW AS BLACK
        for i,p in enumerate(pos_arr):
            if i == 0 and find_knn:
                pygame.draw.circle(surface, (255,0,0), (p[0], p[1]), 3)
            else:
                pygame.draw.circle(surface, color_arr[i], (p[0], p[1]), 1)
            if i == KNN_arr[0] and find_knn:
                pygame.draw.circle(surface, (0,0,255), (p[0], p[1]), 3)
            else:
                pygame.draw.circle(surface, color_arr[i], (p[0], p[1]), 1)
            
    
        # UPDATE
        if find_knn:
            pos_arr, theta_arr, KNN_arr = engine.updateAnts_vectorized(pos_arr, theta_arr, motivation, sh, sw, fov_th, find_knn)
        else:
            pos_arr, theta_arr = engine.updateAnts_vectorized(pos_arr, theta_arr, motivation, sh, sw, fov_th, find_knn)
        
        # UPDATE SCREEN AT FPS
        pygame.time.Clock().tick(FPS)
        pygame.display.update()
        
    # QUIT PYGAME
    pygame.quit()

if __name__ == "__main__":
    main()