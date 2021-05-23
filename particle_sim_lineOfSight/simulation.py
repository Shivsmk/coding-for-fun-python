# -*- coding: utf-8 -*-
"""
Created on Sat May  19 09:29:07 2021
@summary: Particle Simulation 2
@author: Shiv Muthukumar
"""

import pygame
import math

def main():
    # CONSTANTS
    sh = 600
    sw = 600
    FPS = 50
    
    # PARAMETERS
    
    # INITIALIZATION
    pygame.init()
    surface = pygame.display.set_mode((sh, sw))
    clock = pygame.time.Clock()
    
    # CLASS DEF
    class Particle():
        def __init__(self,x,y):
            self.x = x
            self.y = y
        
        def draw_body(self):
            pygame.draw.circle(surface, (0, 255, 0), (int(self.x), int(self.y)), 20)
        
        def projection_points(self):
            n = 6
            #r = 40
            for i in range(n):
                print(360/n*i)
    
    # PARTICLE INITIALIZATION
    particles = [Particle(sw/2, sh/2)]
    for particle in particles:
        particle.projection_points()
    
    # GAME LOOP
    while True:
        # EXIT GAME LOOP ON SCREEN CLOSE
        if pygame.event.peek(pygame.QUIT):
            break
        
        # SIMULATION MAGIC
        surface.fill((255, 255, 255))
        
        # DRAW
        for particle in particles:
            particle.draw_body()
        
        # GAME UPDATES
        pygame.display.update()
        clock.tick(FPS)
    
    # QUIT PYGAME
    pygame.quit()

if __name__ == "__main__":
    main()