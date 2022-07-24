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

    def goto_ppoint(self):
        closest_dist = 10000
        for ppoint in self.environment.ppoints:
            dx = ppoint.x - self.x
            dy = ppoint.y - self.y
            dist = np.sqrt(dx**2+dy**2)
            if dist < closest_dist:
                closest_ppoint = ppoint
                closest_dist = dist
                vect = ppoint.position() - self.position()
        vect = vect / np.linalg.norm(vect)
        return vect

    def goto_line(self):
        line = self.environment.line
        vect_b = 0
        if self.position()[0] > line.point1[0]:
            vect_b = line.point1 - self.position()
        if self.position()[0] < line.point0[0]:
            vect_b = line.point0 - self.position()
        p_line = (self.x + line.a*(self.y - line.b))/(1+line.a**2)*np.array([1, line.a])+ np.array([0, line.b])
        vect_p = p_line-self.position()
        vect = vect_b+vect_p
        return vect / np.linalg.norm(vect)

    def avoid_wall(self):
        from constants import wall_threshold
        vect = np.array([0,0])
        avoid = False
        if self.x < wall_threshold:
            vect[0] = vect[0]+1
            avoid = True
        if self.x > self.environment.width - wall_threshold:
            vect[0] = vect[0] - 1
            avoid = True
        if self.y < wall_threshold:
            vect[1] = vect[1] + 1
            avoid = True
        if self.y > self.environment.height - wall_threshold:
            vect[1] = vect[1] - 1
            avoid = True
        if avoid:
            vect = vect / np.linalg.norm(vect)
        return vect

    def final_v(self, cohese=True, avoid=True, align=True, follow=False, go_point=False, go_line=False):
        from constants import w_wall, w_cohesion, w_avoidance, w_alignment, w_follow, w_gopoint, w_goline
        from constants import k, avoidance_radius
        neighbors, distances = self.sense_neighbors(k)
        self.command_v = 0

        self.command_v = self.command_v +self.avoid_wall()*w_wall
        if cohese:
            neighbors_cohese = neighbors
            self.command_v = self.command_v + self.cohesion(neighbors_cohese)*w_cohesion
        if avoid:
            neighbors_avoid = []
            for i in range(len(distances)):
                if distances[i] < avoidance_radius:
                    neighbors_avoid.append(neighbors[i])
            self.command_v =  self.command_v + self.avoidance(neighbors_avoid)*w_avoidance
        if align:
            neighbors_align = neighbors
            self.command_v = self.command_v + self.alignment(neighbors_align)*w_alignment
        if follow:
            self.command_v = self.command_v + self.follow_leader()*w_follow
        if go_point:
            self.command_v = self.command_v + self.goto_ppoint()*w_gopoint
        if go_line:
            self.command_v = self.command_v + self.goto_line()*w_goline