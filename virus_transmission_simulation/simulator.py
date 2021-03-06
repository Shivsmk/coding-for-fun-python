# -*- coding: utf-8 -*-
"""
Created on Sat May  8 21:29:07 2021
@summary: Exporing pymunk with pygame for particle simulations
@author: Shiv Muthukumar
@motivation: [https://www.youtube.com/watch?v=yJK5J8a7NFs&t=2070s,
              https://www.youtube.com/playlist?list=PL_N_kL9gRTm8lh7GxFHh3ym1RXi6I6c50]
"""

import random

import pygame
import pymunk


def main():
    # CONSTANTS
    sh = 750
    sw = 1400
    FPS = 50
    
    # PARAMETERS
    population = 3000
    ball_radius = 5
    ball_velocity = 100
    force_infection = False
    toggle_vaccination = False
    vaccination_rate = 0.01
    
    # COLLISION TYPE PARAMETERS
    infect_type = population + 2
    recovered_type = population + 3
    dead_type = population + 4
    vaccine_type = population + 5
    
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
            self.init_collision_type = 0
            self.infection_history = 0
            self.infected = False
            self.recovered = False
            self.dead = False
            self.vaccine = False
            self.infection_rate = 0.5
            self.survival_rate = 0.001
            self.recovery_time = 200
            
            space.add(self.body, self.shape)
            
        def draw(self):
            if self.infected:
                pygame.draw.circle(display,(255, 0, 0), convert_coordinates(self.body.position), ball_radius)
            elif self.recovered:
                pygame.draw.circle(display,(0, 0, 255), convert_coordinates(self.body.position), ball_radius)
            elif self.dead:
                pygame.draw.circle(display,(64, 64, 64), convert_coordinates(self.body.position), ball_radius)
            elif self.vaccine:
                pygame.draw.circle(display,(255,105,180), convert_coordinates(self.body.position), ball_radius)
            else:
                pygame.draw.circle(display,(0, 255, 0), convert_coordinates(self.body.position), ball_radius)
        
        def infect(self, space=0, arbiter=0, data=0):
            if random.uniform(0,1) < self.infection_rate or force_infection:
                self.infected = True
                self.shape.collision_type = infect_type
        
        def nowDead(self):
            self.dead = True
            self.infected = False
            self.recovered = False
            self.body.velocity = 0, 0
            self.shape.density = 100000
            self.shape.collision_type = dead_type
        
        def normalcy(self):
            self.recovered = False
            self.infected = False
            self.infection_history = 0
            self.shape.collision_type = self.init_collision_type
            
        def recovery(self):
            self.recovered = True
            self.infected = False
            self.shape.collision_type = recovered_type
            
        def vaccinated(self):
            self.vaccine = True
            self.recovered = False
            self.infected = False
            self.infection_rate = 0.2 * self.infection_rate
            self.shape.collision_type = vaccine_type
        
        def pass_time(self, space=0, arbiter=0, data=0):
            if not self.dead:
                # INCREMENT HISTORY OF INFECTION IF INFECTED OR RECOVERED
                if self.infected or self.recovered:
                        self.infection_history += 1
                # RETURN TO NORMALCY IF INFECTION HISTORY MORE THAN 10x REQUIRED RECOVERY TIME
                if self.infection_history >= 10 * self.recovery_time:
                    self.normalcy()
                # SET TO RECOVERY IF INFECTION HISTORY MORE THAN REQUIRED RECOVERY TIME
                elif self.infection_history >= self.recovery_time:
                    self.recovery()
                # SMALL CHANCE FOR RECOVERED PERSON TO DIE DUE TO INFECTION HISTORY
                if self.recovered and random.uniform(0, 1) < self.survival_rate:
                        self.nowDead()
                # HIGH CHANCE FOR INFECTED PERSON TO DIE DUE TO INFECTION
                if self.infected and random.uniform(0, 1) < 2 * self.survival_rate:
                        self.nowDead()
                # CHANCE FOR A NORMAL TO GET vaccinATED
                if toggle_vaccination and not self.infected and not self.recovered and random.uniform(0, 1) < vaccination_rate:
                    self.vaccinated()
            
        
        def first_infect(self, space=0, arbiter=0, data=0):
            self.infected = True
            self.shape.collision_type = infect_type
            
    
    class Wall():
        def __init__(self, p1, p2):
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
            self.p1 = p1
            self.p2 = p2
            self.shape = pymunk.Segment(self.body, self.p1, self.p2, 5)
            self.shape.elasticity = 1
            space.add(self.body,self.shape)
        
        def draw(self):
            pygame.draw.line(display, (0, 0, 0), convert_coordinates(self.p1), convert_coordinates(self.p2), 5)
    
    # FUNCTIONS
    def convert_coordinates(point):
        return int(point[0]), sh-int(point[1])
    
    # PARTICLE INITIALIZATION AS LIST OF PARTICLES
    balls = [Ball(random.randint(ball_radius,sw-ball_radius),random.randint(ball_radius,sh-ball_radius)) for i in range(population)]
    
    # SET COLLISION HANDLER
    for i in range(1, population+1):
        balls[i-1].shape.collision_type = i
        balls[i-1].init_collision_type = i
        handler = space.add_collision_handler(i, infect_type)
        handler.separate = balls[i-1].infect
    
    # INFECT A BALL AT RANDOM
    random.choice(balls).first_infect()
    
    # SET WALLS
    walls = [Wall((0,0), (sw,0)),
            Wall((sw,0), (sw,sh)),
            Wall((sw,sh), (0,sh)),
            Wall((0,sh), (0,0))]
    
    # SETTING ADDITIONAL BARRIERS
    #walls.append(Wall((sw/2,50), (sw/2,sh-50)))
    #walls.append(Wall((50,sh/2), (sw-50,sh/2)))
    
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
            ball.pass_time()
        
        # GAME UPDATES
        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)
    
    # QUIT PYGAME
    pygame.quit()
    
    # STAT COLLECTION
    count_dead = sum(p.dead for p in balls)
    count_vaccinated = sum(p.vaccine for p in balls)
    count_alive = population - count_dead - count_vaccinated
    print("Starting population:",population)
    print("Post-Infection Dead:", count_dead)
    print("Post-Infection Alive", count_alive)
    print("vaccinated:", count_vaccinated)

if __name__ == "__main__":
    main()
