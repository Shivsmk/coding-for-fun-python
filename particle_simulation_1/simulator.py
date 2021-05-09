# -*- coding: utf-8 -*-
"""
Created on Sat May  8 21:29:07 2021
@summary: Exporing pymunk with pygame for particle simulations
@author: Shiv Muthukumar
"""

import pygame
import pymunk
import random


def main():
    # CONSTANTS
    sh = 600
    sw = 600
    FPS = 50
    
    # PARAMETERS
    population = 100
    ball_radius = 10
    ball_velocity = 100
    
    # INITIALIZATION
    pygame.init()
    display = pygame.display.set_mode((sw, sh))
    clock = pygame.time.Clock()
    space = pymunk.Space()
    
    # CLASSES
    class Ball():
        def __init__(self, x, y):
            self.body = pymunk.Body()
            self.body.position = x, y
            self.body.velocity = random.uniform(-ball_velocity,ball_velocity), random.uniform(-ball_velocity,ball_velocity)
            self.shape = pymunk.Circle(self.body, ball_radius)
            self.shape.elasticity = 1
            self.shape.density = 1
            space.add(self.body, self.shape)
            
        def draw(self):
            pygame.draw.circle(display,(0, 255, 0), convert_coordinates(self.body.position), ball_radius)
        
    # FUNCTIONS
    def convert_coordinates(point):
        return int(point[0]), sh-int(point[1])
    
    # PARTICLE INITIALIZATION
    balls = [Ball(random.randint(ball_radius,sw-ball_radius),random.randint(ball_radius,sh-ball_radius)) for i in range(population)]
    
    # GAME LOOP
    while True:
        # EXIT GAME LOOP ON SCREEN CLOSE
        if pygame.event.peek(pygame.QUIT):
            break
        
        # RESET SCREEN
        display.fill((255, 255, 255))
        
        # DRAW AND UPDATE
        for ball in balls:
            ball.draw()
        
        # GAME UPDATES
        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)
    
    # QUIT PYGAME
    pygame.quit()

if __name__ == "__main__":
    main()