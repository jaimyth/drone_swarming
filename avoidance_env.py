import pygame as pg
import random
import numpy as np
from agent import Agent
from agent_flock import Agent_Flock
from environment import Environment
import constants
from agent_id import *
width, height = (800, 600)
bg_color = (255, 200, 180)

env = Environment(width=width, height=height, bg_color=bg_color)
env.update_environment()
ag1 = Agent(environment= env, x= 100, y = 200, color = [255,0,0], id=get_id())
random.seed(10)
env.add_agent(ag1)
for i in range(10):
    ag = Agent_Flock(environment=env, x = random.randint(150, 250), y = random.randint(195, 205), id=get_id())
    env.add_agent(ag)


run =  True

while run:
    t = pg.time.get_ticks()
    ag1.vx = 20
    env.clear_environment()

    for i in env.agents[1:]:
        i.final_v(cohese=False, avoid=True)
        i.update_velocity()
        i.update_position()
        i.draw_history(env.screen)
        i.draw_desv(env.screen)
    env.update_agents()
    ag1.draw_history(env.screen)
    centroid = ag1.centroid_neighbors(ag1.sense_neighbors(5)[0])
    pg.draw.circle(env.screen, (0, 0, 255), centroid.astype(int),
                   5, 0)
    env.draw_agents()
    pg.time.delay(int(constants.dt*4000))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    env.update_environment()