import numpy as np
import pygame as pg
from straight_line import S_line

def create_polygon_points(n, r, center):
        points = np.zeros((n, 2))
        points[0] = np.array([center[0], center[1]+r])
        theta = np.pi / 2
        dTheta = 2 * np.pi / n

        for i in range(1, n):
            theta += dTheta
            points[i] = np.array([center[0] + r * np.cos(theta), center[1] + r * np.sin(theta)])
        return points

class Shape:

    def __init__(self, environment, points, closed = True):
        self.points = points
        self.env = environment
        self.closed = closed
        self.lines = self.generate_lines()
        self.center = self.calculate_center()


    def generate_lines(self):
        lines = []
        for i in range(len(self.points[:-1])):
            line = S_line(self.env, self.points[i], self.points[i+1])
            lines.append(line)

        if self.closed:
            line = S_line(self.env, self.points[-1], self.points[0])
            lines.append(line)
        return lines

    def calculate_center(self):
        center_x = np.average(self.points[:,0])
        center_y = np.average(self.points[:,1])
        return np.array([center_x, center_y])

    def draw_shape(self):
        for line in self.lines:
            line.draw()