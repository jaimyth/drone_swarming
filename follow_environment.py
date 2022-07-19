import pygame as pg
import random
import numpy as np
from agent import Agent
from agent_flock import Agent_Flock
from environment import Environment
import constants
from agent_id import *
width, height = (1200, 700)
bg_color = (255, 200, 180)

env = Environment(width=width, height=height, bg_color=bg_color)
env.update_environment()
ag1 = Agent(environment= env, x= 100, y = 300, color = [255,0,0], id=get_id())

random.seed(2)
env.add_agent(ag1)
n = 10

x_pos = 90
y_pos = np.linspace(0,260, n)
for i in range(n):
    #ag = Agent_Flock(environment=env, x = random.randint(150, 250), y = random.randint(150, 250), id=get_id())
    ag = Agent_Flock(environment=env, x = x_pos, y = y_pos[i], id=get_id())
    env.add_agent(ag)


run =  True

env.leader = ag1
print(env.leader)

while run:
    t = pg.time.get_ticks()
    #ag1.v = np.array([80,0])
    vy = 250*np.sin(t/1000)
    vx = 50
    ag1.v = np.array([vx, vy])
    env.clear_environment()

    for i in env.agents[1:]:
        i.final_v(cohese=False, avoid=True, align=False, follow=True)
        i.update_velocity()
        i.update_position()
        i.draw_history(env.screen)
        #i.draw_desv(env.screen)
    env.update_agents()
    ag1.draw_history(env.screen)
    centroid = ag1.centroid_neighbors(ag1.sense_neighbors(5)[0])
    pg.draw.circle(env.screen, (0, 0, 255), centroid.astype(int),
                   5, 0)
    env.draw_agents()
    pg.time.delay(int(constants.dt*2000))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                for i in env.agents:
                    i.reset()
    env.update_environment()