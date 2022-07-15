import pygame as pg
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
ag1 = Agent(environment= env, x= 100, y = 200, id=get_id())
env.add_agent(ag1)
for i in range(10):
    ag = Agent_Flock(environment=env, x = i*100, y=300+i*20, id=get_id())
    env.add_agent(ag)



run =  True

while run:
    t = pg.time.get_ticks()
    vy = 100*np.sin(t/1000)
    ag1.vx = 10
    ag1.vy = vy
    env.clear_environment()
    for i in env.agents[1:]:
        i.final_v(cohese=True, avoid=True)
        i.update_velocity()
        i.draw_history(env.screen)

    env.update_agents()
    ag1.draw_history(env.screen)
    centroid = ag1.centroid_neighbors(ag1.sense_neighbors(30)[0])
    pg.draw.circle(env.screen, (0, 0, 255), centroid.astype(int),
                   5, 0)
    env.draw_agents()
    pg.time.delay(int(constants.dt*1000))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    env.update_environment()