import numpy as np
import pygame as pg
from agent import Agent

class Agent_Flock(Agent):

    def cohesion(self):
        from constants import w_cohesion
        neighbors = self.sense_neighbors(6, 500)
        centroid = self.centroid_neighbors(neighbors)
        diff = centroid - self.position()
        centroid_v = diff/np.linalg.norm(diff)
        return centroid_v

    def avoidance(self):
        from constants import avoidance_radius
        neighbors = self.sense_neighbors(6, avoidance_radius)
        avoidance_v = np.array([0,0])
        if len(neighbors) == 0:
            return avoidance_v
        for i in neighbors:
            d_vector = i.position() - self.position()
            avoidance_v = avoidance_v -  d_vector
        avoidance_v = avoidance_v / np.linalg.norm(avoidance_v)
        if any(np.isnan(avoidance_v)):
            print('NaN')
            return np.array([0,0])
        else:
            return avoidance_v

    def final_v(self, cohese=True, avoid=True):
        from constants import w_cohesion, w_avoidance
        self.command_v = 0
        if cohese:
            self.command_v += self.cohesion()*w_cohesion
        if avoid:
            self.command_v += self.avoidance()*w_avoidance


