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

    def distribute(self):
        from constants import avoidance_radius
        n_agents = len(self.environment.agents)
        circum = n_agents*avoidance_radius*1.2
        r = circum/np.pi/2
        centroid = self.environment.global_centroid
        vect_centroid = centroid - self.position()

        dist_centroid = np.linalg.norm(vect_centroid)
        vect_t = np.array([0,0])
        vect_n = np.array([-vect_centroid[1], vect_centroid[0]])
        if dist_centroid > r:
            vect_t = vect_t + vect_centroid + vect_n
        if dist_centroid < r:
            vect_t = vect_t - vect_centroid + vect_n

        if np.linalg.norm(vect_t) != 0:
            vect_t = vect_t/np.linalg.norm(vect_t)
        return vect_t

    def flower(self, n_petal):

        centroid = self.environment.global_centroid
        vect_centroid = centroid - self.position()
        theta = np.arctan(vect_centroid[1] / vect_centroid[0])
        if vect_centroid[0] < 0:
            theta = np.arctan(vect_centroid[1]/vect_centroid[0]) + np.pi
        if vect_centroid[1] < 0 and vect_centroid[0] > 0:
            theta = np.arctan(vect_centroid[1]/vect_centroid[0]) + np.pi*2

        n_petal = n_petal / 2
        r = abs(175 * np.cos(n_petal * theta))
        r = max(50, r)

        dist_centroid = np.linalg.norm(vect_centroid)
        vect_t = np.array([0,0])

        if dist_centroid > r:
            vect_t = vect_t + vect_centroid
        if dist_centroid < r:
            vect_t = vect_t - vect_centroid

        if np.linalg.norm(vect_t) != 0:
            vect_t = vect_t/np.linalg.norm(vect_t)
        return vect_t

    def polygon(self, n_polygon):
        centroid = self.environment.global_centroid
        vect_centroid = centroid - self.position()
        theta = np.arctan(vect_centroid[1] / vect_centroid[0])
        if vect_centroid[0] < 0:
            theta = np.arctan(vect_centroid[1]/vect_centroid[0]) + np.pi
        if vect_centroid[1] < 0 and vect_centroid[0] > 0:
            theta = np.arctan(vect_centroid[1]/vect_centroid[0]) + np.pi*2
        dist_centroid = np.linalg.norm(vect_centroid)
        vect_t = np.array([0,0])
        kl = 200

        segment_angles = np.deg2rad(np.linspace(0, 360, n_polygon+1))[1:]
        #r = kl*np.cos(np.pi / n_polygon) / np.cos(2 * np.pi * (n_polygon * theta) % 1 / n_polygon - np.pi / n_polygon)

        print(np.rad2deg(segment_angles))
        #todo: Complicated math
        segment_coefficients = [[1,1], [-1,1], [-1,-1], [1,-1]]
        segment_coefficients = [ [1,0], [1,1], [0,1], [-1,1], [1,0], [-1,-1], [0,-1], [1,-1] ]

        for i, angle in enumerate(segment_angles):
            if theta <= angle:
                coefficient = segment_coefficients[i]
                r = abs(kl/(coefficient[0]*np.cos(theta)+coefficient[1]*np.sin(theta)))
                break

        if dist_centroid > r:
            vect_t = vect_t + vect_centroid
        if dist_centroid < r:
            vect_t = vect_t - vect_centroid

        if np.linalg.norm(vect_t) != 0:
            vect_t = vect_t/np.linalg.norm(vect_t)
        return vect_t


    def center(self):
        from constants import center_r
        vect = np.array([0,0])
        center_screen = np.array([self.environment.width/2, self.environment.height/2])
        dist = np.linalg.norm(center_screen - self.position())
        if dist > center_r:
            vect = center_screen - self.position()
            vect = vect/np.linalg.norm(vect)
        return vect

    def final_v(self, cohese=True, avoid=True, align=True, follow=False, go_point=False, go_line=False, go_shape = False
                , distribute = False, center=False, n_petal=0, n_polygon =0):
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
            self.command_v = self.command_v + self.avoidance(neighbors_avoid)*w_avoidance
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
            self.command_v = self.command_v + self.distribute() * w_distribute
        if center:
            self.command_v = self.command_v + self.center()*w_center
        if n_petal:
            self.command_v = self.command_v + self.flower(n_petal) * w_distribute
        if n_polygon:
            self.command_v = self.command_v + self.polygon(n_polygon) * w_distribute