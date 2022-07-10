import numpy as np
import pygame as pg

class Agent:
    def __init__(self):
        import constants
        self.dt = constants.dt

        self.x = 0
        self.y = 0

        self.v =0
        self.command_v = 0

        self.vx = 0
        self.vy = 0

    def update(self):
        self.x += self.dt * self.vx
        self.y += self.dt*self.vy
        #print(self.x, self.y)

    def draw(self, screen):
        pg.draw.circle(screen, (0, 255, 0), [int(self.x), int(self.y)],
                       5, 0)

