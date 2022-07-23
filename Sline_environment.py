import pygame as pg
import random
import numpy as np
from agent import Agent
from straight_line import S_line
from agent_flock import Agent_Flock
from environment import Environment
import constants
from agent_id import *
width, height = (1200, 700)
bg_color = (255, 200, 180)

env = Environment(width=width, height=height, bg_color=bg_color)
env.update_environment()


random.seed(2)

n = 20
n_pp = 200
x_pos = 90
y_pos = np.linspace(40,550, n)

point0 = np.array([0, 100])
point1 = np.array([env.width, 900])

sline = S_line(env, point0, point1)
env.line = sline

for i in range(n):
    #ag = Agent_Flock(environment=env, x = random.randint(150, 250), y = random.randint(150, 250), id=get_id())
    ag = Agent_Flock(environment=env, x = y_pos[i]+5*i, y = y_pos[i], id=get_id())
    env.add_agent(ag)

run =  True
cohese = False

while run:
    t = pg.time.get_ticks()

    env.clear_environment()

    for i, ag in enumerate(env.agents):
        ag.final_v(cohese=cohese, avoid=True, align=False, follow=False, go_point=False, go_line=True)
        ag.update_velocity()
        ag.update_position()
        ag.draw_history(env.screen)
    env.line.draw()
    env.update_agents()
    env.draw_agents()
    pg.time.delay(int(constants.dt*2000))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                for i in env.agents:
                    i.reset_position()
            if event.key == pg.K_c:
                cohese = not cohese
            if event.key == pg.K_h:
                for ag in env.agents:
                    ag.reset_history()
    env.update_environment()