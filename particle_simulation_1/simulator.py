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
    
    class Wall():
        def __init__(self, p1, p2):
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
            self.p1 = p1
            self.p2 = p2
            self.shape = pymunk.Segment(self.body, self.p1, self.p2, 1)
            self.shape.elasticity = 1
            space.add(self.body,self.shape)
        
        def draw(self):
            pygame.draw.line(display, (0, 0, 0), convert_coordinates(self.p1), convert_coordinates(self.p2), 1)
    
    # FUNCTIONS
    def convert_coordinates(point):
        return int(point[0]), sh-int(point[1])
    
    # PARTICLE INITIALIZATION AS LIST OF PARTICLES
    balls = [Ball(random.randint(ball_radius,sw-ball_radius),random.randint(ball_radius,sh-ball_radius)) for i in range(population)]
    
    # SET WALLS
    walls = [Wall((0,0), (sw,0)),
            Wall((sw,0), (sw,sh)),
            Wall((sw,sh), (0,sh)),
            Wall((0,sh), (0,0))]
    
    # GAME LOOP
    while True:
        # EXIT GAME LOOP ON SCREEN CLOSE
        if pygame.event.peek(pygame.QUIT):
            break
        
        # RESET SCREEN
        display.fill((255, 255, 255))
        
        # DRAW AND UPDATE
        for wall in walls:
            wall.draw()
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