import numpy as np
import pygame as pg
import pygame.freetype
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
        self.font = self.initialise_font()
        self.global_centroid = 0

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

    def initialise_font(self):
        font = pygame.freetype.SysFont('arial', 20)
        return font

    def render_text(self, msg, position):
        self.font.render_to(self.screen, (position[0], position[1]), msg, [0,0,0])

    def update_environment(self):
        pg.display.flip()

    def clear_environment(self):
        self.screen.fill(self.bg_color)

    def draw_agents(self):
        for i in self.agents:
            i.draw(self.screen)

    def draw_shape(self):
        self.shape.draw_shape()

    def calculate_global_centroid(self):
        centroid = np.array([0,0])
        for agent in self.agents:
            centroid = (centroid +  agent.position())# / np.linalg.norm(i.position())
        centroid = centroid / (len(self.agents))
        centroid = centroid# / np.linalg.norm(centroid)
        return centroid