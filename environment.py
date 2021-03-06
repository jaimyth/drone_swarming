import numpy as np
import pygame as pg

class Environment:

    def __init__(self, width, height, bg_color):
        self.width = width
        self.height = height
        self.agents = []
        self.ppoints = []
        self.line = None
        self.lines = []
        self.shape = None
        self.leader = None
        self.bg_color = bg_color
        self.screen = self.initialise_environment()

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_ppoint(self, point):
        self.ppoints.append(point)

    def update_agents(self):
        for i in self.agents:
            i.update_position()

    def initialise_environment(self):
        pg.init()
        screen = pg.display.set_mode((self.width, self.height))
        screen.fill(self.bg_color)
        return screen

    def update_environment(self):
        pg.display.flip()

    def clear_environment(self):
        self.screen.fill(self.bg_color)

    def draw_agents(self):
        for i in self.agents:
            i.draw(self.screen)

    def draw_shape(self):
        self.shape.draw_shape()
