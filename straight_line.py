import numpy as np
import pygame as pg



class S_line:

    #straight line with the form y = ax + b
    def __init__(self, environment, point0, point1):
        self.environment = environment
        self.point0 = point0
        self.point1 = point1
        if self.point0[0] == self.point1[0]:
            self.point1[0] = self.point0[0]+0.0001
        self.a = (point1[1] - point0[1]) / (point1[0] - point0[0])
        self.b = point0[1] - self.a * point0[0]
        self.x_bounds = np.array([point0[0], point1[0]])


    def calc_y(self, x):
        return self.a*x + self.b

    def calc_x(self, y):
        return (y - self.b)/self.a

    def draw(self):
        pg.draw.line(self.environment.screen, [0,0,0], self.point0, self.point1)

