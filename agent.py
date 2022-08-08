import numpy as np
import pygame as pg

class Agent:
    def __init__(self, environment, x=0, y=0, color = [0,255,0], id=0):
        import constants
        self.environment = environment
        self.color = color
        self.dt = constants.dt
        self.x = x
        self.y = y
        self.x_init = x
        self.y_init = y
        self.x_hist = [x, x]
        self.y_hist = [y, y]

        self.v =np.array([0,0])
        self.command_v = 0


        self.id = id    #unique id to identify each agent

    def update_velocity(self):
        from constants import v_factor
        self.v = (1-v_factor)*self.v + v_factor*self.command_v

    def update_position(self):
        self.x += self.dt * self.v[0]
        self.y += self.dt * self.v[1]
        # if self.id == 10:
        #     print(f'{self.x, self.y}, id = {self.id}')
        self.x_hist.append(self.x)
        self.y_hist.append(self.y)

    def position(self):
        return np.array([self.x, self.y])

    def sense_neighbors(self, k = 5):
        agents = self.environment.agents
        if k > len(agents):
            #print(f'n = {len(agents)}, k changed from {k} to {len(agents)}')
            k = len(agents)
        if k==1:
            return [], []
        distances = []
        for i in agents:
            from constants import collision_radius
            dx = i.x - self.x
            dy = i.y - self.y
            dist = np.sqrt(dx**2+dy**2)
            distances.append(dist)
            if dist < collision_radius and self.id != i.id:
                self.color = [0,0,0]
                i.color = [0,0,0]
        order = np.argsort(distances)[1:k+1]

        neighbor_agents = []
        distance_sorted = []
        for j in order:
            neighbor_agents.append(agents[j])
            distance_sorted.append(distances[j])
        return neighbor_agents, distance_sorted

    def centroid_neighbors(self, agent_list):
        centroid = np.array([0,0])
        for i in agent_list:
            centroid = (centroid +  i.position())# / np.linalg.norm(i.position())
        centroid = centroid / (len(agent_list))
        centroid = centroid# / np.linalg.norm(centroid)
        return centroid

    def draw(self, screen):
        from constants import size_agents
        pg.draw.circle(screen, self.color, [int(round(self.x,0)), int(round(self.y,0))],
                       size_agents, 0)

    def draw_history(self, screen):
        hist = list(zip(self.x_hist,self.y_hist))
        pg.draw.lines(screen, (0, 0, 0), False, hist)

    def draw_desv(self, screen):
        pg.draw.line(screen, (255,255,255), self.position(), self.position()+(self.command_v*2).astype(int))

    def reset_position(self):
        self.x = self.x_init
        self.y = self.y_init
        self.v = np.array([0,0])
        self.x_hist = [self.x, self.x]
        self.y_hist = [self.y, self.y]

    def reset_history(self):
        self.x_hist = [self.x, self.x]
        self.y_hist = [self.y, self.y]