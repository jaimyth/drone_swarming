import pygame as pg
import numpy as np
from agent import Agent
from environment import Environment
import constants
width, height = (800, 600)
bg_color = (255, 200, 180)

env = Environment(width=width, height=height, bg_color=bg_color)
env.update_environment()
ag1 = Agent(100, 200)
ag1.vx = 10

env.add_agent(ag1)

run =  True

while run:



    t = pg.time.get_ticks()
    vy = 100*np.sin(t/1000)
    ag1.vy = vy
    env.clear_environment()
    env.update_agents()
    ag1.draw_history(env.screen)
    env.draw_agents()
    pg.time.delay(int(constants.dt*1000))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    env.update_environment()