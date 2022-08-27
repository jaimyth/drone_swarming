import numpy as np
import pygame as pg
from agent import Agent
import sys
EPSILON = sys.float_info.epsilon  # Smallest possible difference.

def convert_to_rgb(minval, maxval, val, colors):

    #https://stackoverflow.com/questions/20792445/calculate-rgb-value-for-a-range-of-values-to-create-heat-map/71503186#71503186

    # `colors` is a series of RGB colors delineating a series of
    # adjacent linear color gradients between each pair.

    # Determine where the given value falls proportionality within
    # the range from minval->maxval and scale that fractional value
    # by the total number in the `colors` palette.
    i_f = float(val-minval) / float(maxval-minval) * (len(colors)-1)

    # Determine the lower index of the pair of color indices this
    # value corresponds and its fractional distance between the lower
    # and the upper colors.
    i, f = int(i_f // 1), i_f % 1  # Split into whole & fractional parts.

    # Does it fall exactly on one of the color points?
    if f < EPSILON:
        return colors[i]
    else: # Return a color linearly interpolated in the range between it and
          # the following one.
        (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i+1]
        return int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))


class Agent_Flock(Agent):

    def cohesion(self, delta_positions):
        centroid = self.centroid_neighbors(delta_positions)
        #diff = centroid - self.position()
        centroid_v = centroid/np.linalg.norm(centroid)
        return centroid_v

    def avoidance(self, delta_positions):
        avoidance_v = np.array([0,0])
        if len(delta_positions) == 0:
            return avoidance_v
        avoidance_v = avoidance_v - np.sum(delta_positions, axis =0)
        if np.linalg.norm(avoidance_v) != 0:
            avoidance_v = avoidance_v/np.linalg.norm(avoidance_v)
        return avoidance_v

    def alignment(self, delta_velocities):
        align_v = np.array([0,0])
        if len(delta_velocities) == 0:
            return align_v
        align_v = align_v + np.sum(delta_velocities, axis=0)
        if np.linalg.norm(align_v) != 0:
            align_v = align_v/np.linalg.norm(align_v)
        return align_v

    def follow_leader(self):
        follow_v = np.array([0,0])
        follow_pos = np.array([0,0])
        leader = self.environment.leader
        if leader is None or np.linalg.norm(leader.v)==0:
            return follow_v

        delta_v = leader.v - self.v
        #delta_pos = leader.position() - self.position()
        if np.linalg.norm(delta_v) != 0:
            delta_v = delta_v/np.linalg.norm(delta_v)
        #follow_pos = delta_pos / np.linalg.norm(delta_pos)
        return delta_v

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

    def flower(self, scale=175, n_petal=3):

        centroid = self.environment.global_centroid
        vect_centroid = centroid - self.position()
        theta = np.arctan(vect_centroid[1] / vect_centroid[0])
        if vect_centroid[0] < 0:
            theta = np.arctan(vect_centroid[1]/vect_centroid[0]) + np.pi
        if vect_centroid[1] < 0 and vect_centroid[0] > 0:
            theta = np.arctan(vect_centroid[1]/vect_centroid[0]) + np.pi*2

        n_petal = n_petal / 2
        r = abs(scale * np.cos(n_petal * theta))
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

    def shape(self, scale, n, m, k):
        centroid = self.environment.global_centroid
        vect_centroid = centroid - self.position()
        theta = np.arctan(vect_centroid[1] / vect_centroid[0])
        if vect_centroid[0] < 0:
            theta = np.arctan(vect_centroid[1]/vect_centroid[0]) + np.pi
        if vect_centroid[1] < 0 and vect_centroid[0] > 0:
            theta = np.arctan(vect_centroid[1]/vect_centroid[0]) + np.pi*2
        dist_centroid = np.linalg.norm(vect_centroid)

        r = scale * np.cos((2 * np.arcsin(k) + np.pi * m) / (2 * n)) / (
            np.cos((2 * np.arcsin(k * np.cos(n * theta)) + np.pi * m) / (2 * n)))
        vect_t = np.array([0,0])

        if dist_centroid > r:
            vect_t = vect_t + vect_centroid
        if dist_centroid < r:
            vect_t = vect_t - vect_centroid

        if np.linalg.norm(vect_t) != 0:
            vect_t = vect_t / np.linalg.norm(vect_t)
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

    def gradient(self):
        centroid = self.environment.global_centroid
        vect_centroid = centroid - self.position()
        theta = np.arctan(vect_centroid[1] / vect_centroid[0])
        if vect_centroid[0] < 0:
            theta = np.arctan(vect_centroid[1]/vect_centroid[0]) + np.pi
        if vect_centroid[1] < 0 and vect_centroid[0] > 0:
            theta = np.arctan(vect_centroid[1]/vect_centroid[0]) + np.pi*2
        minval, maxval = 0, 360
        colors = [(0,0,255), (255,0,0), (0,255,0), (255,0,0),(0,0,255)]
        r,g,b = convert_to_rgb(minval, maxval, np.rad2deg(theta), colors)
        self.color = (r,g,b)

    def final_v(self, shape_factors, cohese=False, avoid=True, align=False, follow=False, center=False, flower=False, shape=False):
        from constants import w_wall, w_cohesion, w_avoidance, w_alignment, w_follow, w_distribute, w_center
        from constants import k, avoidance_radius
        delta_positions, delta_velocities = self.sense_neighbors(k)
        delta_p_leader = self.environment.leader.position() - self.position()
        delta_v_leader = self.environment.leader.v - self.v
        self.command_v = 0

        self.command_v = self.command_v +self.avoid_wall()*w_wall
        if cohese:
            neighbors_cohese = delta_positions
            self.command_v = self.command_v + self.cohesion(neighbors_cohese)*w_cohesion
        if avoid:
            neighbors_avoid = []
            for i in delta_positions:
                if np.linalg.norm(i) < avoidance_radius:
                    neighbors_avoid.append(i)
            if np.linalg.norm(delta_p_leader) < avoidance_radius:
                neighbors_avoid.append(delta_p_leader)
            self.command_v = self.command_v + self.avoidance(neighbors_avoid)*w_avoidance
        if align:
            neighbors_align = delta_velocities
            self.command_v = self.command_v + self.alignment(neighbors_align)*w_alignment
        if follow:
            self.command_v = self.command_v + self.follow_leader()*w_follow
        if center:
            self.command_v = self.command_v + self.center()*w_center
        if flower:
            self.command_v = self.command_v + self.flower(shape_factors[0], shape_factors[1]) * w_distribute
        if shape:
            self.command_v = self.command_v + self.shape(shape_factors[0], shape_factors[1], shape_factors[2], shape_factors[3])* w_distribute