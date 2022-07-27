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

    def goto_shape(self):
        shortest_dist = 10000
        shortest_vect = None
        for line in self.environment.shape.lines:
            vect_b = 0
            p_line = (self.x + line.a * (self.y - line.b)) / (1 + line.a ** 2) * np.array([1, line.a]) + np.array(
                [0, line.b])
            if p_line[0] < line.point0[0]:
                vect_b = line.point0 - self.position()
            if p_line[0] > line.point1[0]:
                vect_b = line.point1 - self.position()
            vect_p = p_line - self.position()
            vect = vect_b + vect_p
            if np.linalg.norm(vect) < shortest_dist:
                shortest_dist = np.linalg.norm(vect)
                shortest_vect = vect
                if np.linalg.norm(vect) == 0:
                    break
        if np.linalg.norm(shortest_vect) == 0:
            return shortest_vect
        else:
            vect_c = self.environment.shape.center - self.position()
            vect_c = vect_c/np.linalg.norm(vect_c)
            shortest_vect = shortest_vect# + vect_c/1000
        return shortest_vect/np.linalg.norm(shortest_vect)

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

    def distribute(self, neighbors, distances):
        from constants import avoidance_radius
        n_agents = len(self.environment.agents)
        circum = n_agents*avoidance_radius*1.2
        r = circum/np.pi/2
        centroid = self.centroid_neighbors(neighbors)
        vect_centroid = centroid - self.position()
        dist_centroid = np.linalg.norm(vect_centroid)
        vect_t = np.array([0,0])

        if dist_centroid > r:
            vect_t = vect_t + vect_centroid
        if dist_centroid < r:
            vect_t = vect_t - vect_centroid
            if dist_centroid < r - 4:
                print(self.id, self.position(), centroid)

        if np.linalg.norm(vect_t) != 0:
            vect_t = vect_t/np.linalg.norm(vect_t)
        return vect_t

        ''''
        vect_centroid = centroid - self.position()
        dist_centroid = np.linalg.norm(vect_centroid)
        neighbors_2 = neighbors[:2]
        distances_2 = distances[:2]
        neighbors_r = neighbors[2:]
        distances_r = distances[2:]
        d_distribute = 35
        vect_t = np.array([0,0])
        for i, neighbor in enumerate(neighbors_2):
            vect = neighbor.position() - self.position()
            dist_nc = np.linalg.norm(centroid - neighbor.position())
            if dist_nc != dist_centroid:
                vect_t = vect_t - vect_centroid
            if distances_2[i] > d_distribute:
                vect_t = vect_t + vect
            if distances_2[i] < d_distribute:
                vect_t = vect_t - vect
        for j, neighbor in enumerate(neighbors_r):
            vect = neighbor.position() - self.position()
            if distances_r[j] < d_distribute*1.8:
                vect_t = vect_t - vect
        if np.linalg.norm(vect_t) != 0:
            vect_t = vect_t/np.linalg.norm(vect_t)
        return vect_t
        '''
    def center(self):
        from constants import center_r
        vect = np.array([0,0])
        center_screen = np.array([self.environment.width/2, self.environment.height/2])
        dist = np.linalg.norm(center_screen - self.position())
        if dist > center_r:
            vect = center_screen - self.position()
            vect = vect/np.linalg.norm(vect)
        return vect

    def final_v(self, cohese=True, avoid=True, align=True, follow=False, go_point=False, go_line=False, go_shape = False, distribute = False, center=False):
        from constants import w_wall, w_cohesion, w_avoidance, w_alignment, w_follow, w_gopoint, w_goline, w_distribute, w_center
        from constants import k, avoidance_radius, distribute_radius
        neighbors, distances = self.sense_neighbors(k)
        self.command_v = 0

        self.command_v = self.command_v +self.avoid_wall()*w_wall
        if cohese:
            neighbors_cohese = neighbors
            self.command_v = self.command_v + self.cohesion(neighbors_cohese)*w_cohesion
        if avoid:
            neighbors_avoid = []
            neighbors_distribute = []
            for i in range(len(distances)):
                if distances[i] < distribute_radius:
                    neighbors_distribute.append(neighbors[i])
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
        if go_shape:
            self.command_v = self.command_v + self.goto_shape() * w_goline
        if distribute:
            self.command_v = self.command_v + self.distribute(neighbors, distances) * w_distribute
        if center:
            self.command_v = self.command_v + self.center()*w_center