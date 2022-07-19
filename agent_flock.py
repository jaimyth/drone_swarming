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

    def alignment(self, neighbors):
        align_v = np.array([0,0])
        if len(neighbors) == 0:
            return align_v
        for i in neighbors:
            delta_v = i.v - self.v
            align_v = align_v + delta_v
        align_v = (align_v + self.v)
        if align_v[0] == 0 and align_v[1] == 0:
            return align_v
        align_v = align_v / np.linalg.norm(align_v)
        return align_v

    def follow_leader(self):
        follow_v = np.array([0,0])
        follow_pos = np.array([0,0])
        leader = self.environment.leader
        if leader is None:
            return follow_v
        delta_v = leader.v - self.v
        delta_pos = leader.position() - self.position()
        if delta_pos[0] == 0 and delta_pos[1] == 0:
            return follow_pos
        follow_pos = delta_pos / np.linalg.norm(delta_pos)
        return follow_pos

    def final_v(self, cohese=True, avoid=True, align=True, follow=False):
        from constants import w_cohesion, w_avoidance, w_alignment, w_follow
        from constants import k, avoidance_radius
        neighbors, distances = self.sense_neighbors(k)
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
        if align:
            neighbors_align = neighbors
            self.command_v = self.command_v + self.alignment(neighbors_align)*w_alignment
        if follow:
            #print(1, self.command_v)
            self.command_v = self.command_v + self.follow_leader()*w_follow
            #print(2, self.command_v)

