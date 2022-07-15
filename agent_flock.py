import numpy as np
import pygame as pg
from agent import Agent

class Agent_Flock(Agent):

    def cohesion(self, neighbors):
        centroid = self.centroid_neighbors(neighbors)
        diff = centroid - self.position()
        centroid_v = diff/np.linalg.norm(diff)
        return centroid_v

    def avoidance(self, neighbors):
        avoidance_v = np.array([0,0])
        if len(neighbors) == 0:

            return avoidance_v
        for i in neighbors:
            d_vector = i.position() - self.position()
            avoidance_v = avoidance_v -  d_vector
        avoidance_v = avoidance_v / np.linalg.norm(avoidance_v)
        if any(np.isnan(avoidance_v)):
            return np.array([0,0])
        else:
            return avoidance_v

    def final_v(self, cohese=True, avoid=True):
        from constants import w_cohesion, w_avoidance
        from constants import avoidance_radius
        neighbors, distances = self.sense_neighbors(10)
        self.command_v = 0
        if cohese:
            neighbors_cohese = neighbors
            self.command_v += self.cohesion(neighbors_cohese)*w_cohesion
        if avoid:
            neighbors_avoid = []
            for i in range(len(distances)):
                if distances[i] < avoidance_radius:
                    neighbors_avoid.append(neighbors[i])
            self.command_v += self.avoidance(neighbors_avoid)*w_avoidance


