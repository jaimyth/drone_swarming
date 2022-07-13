import numpy as np
import pygame as pg
from agent import Agent

class Agent_Flock(Agent):

    def cohesion(self):
        w_cohesion = 1
        neighbors = self.sense_neighbors(6, 500)
        centroid = self.centroid_neighbors(neighbors)
        diff = centroid - self.position()
        desired_v = w_cohesion*diff
        self.command_v = desired_v