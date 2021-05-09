# -*- coding: utf-8 -*-
"""
Created on Sat May  8 21:29:07 2021
@summary: Exporing pymunk with pygame for particle simulations
@author: Shiv Muthukumar
"""

import pygame
import pymunk

def main():
    # CONSTANTS
    sh = 600
    sw = 600
    FPS = 50
    
    # PARAMETERS
    
    # INITIALIZATION
    pygame.init()
    display = pygame.display.set_mode((sh, sw))
    clock = pygame.time.Clock()
    space = pymunk.Space()
    
    # GAME LOOP
    while True:
        # EXIT GAME LOOP ON SCREEN CLOSE
        if pygame.event.peek(pygame.QUIT):
            break
        
        # SIMULATION MAGIC
        display.fill((255, 255, 255))
        
        # GAME UPDATES
        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)
    
    # QUIT PYGAME
    pygame.quit()

if __name__ == "__main__":
    main()