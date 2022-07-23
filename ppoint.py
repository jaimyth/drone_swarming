import numpy as np
import pygame as pg

class Ppoint:

    def __init__(self, environment, x=0, y=0):
        self.environment = environment
        self.x = x
        self.y = y
        self.color = [0,0,255]

    def position(self):
        return np.array([self.x, self.y])

    def draw(self, screen):
        from constants import size_agents
        pg.draw.circle(screen, self.color, [int(round(self.x,0)), int(round(self.y,0))],
                       size_agents, 0)

