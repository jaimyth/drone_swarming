import pygame as pg
import random
import numpy as np
from agent import Agent
from ppoint import Ppoint
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

n = 11
x_pos = 200
y_pos = np.linspace(200,550, n)



for i in range(n):
    #ag = Agent_Flock(environment=env, x = random.randint(150, 250), y = random.randint(150, 250), id=get_id())
    ag = Agent_Flock(environment=env, x = y_pos[i]+5*i, y = y_pos[i], id=get_id())
    env.add_agent(ag)

run =  True
cohese = False
go_point = False
go_line = False
align = False

r = 200
center = np.array([env.width/2, env.height/2])
point0 = center

pp = Ppoint(env, center[0], center[1])
env.ppoints = [pp]
kt = 0
while run:
    t = pg.time.get_ticks()
    kt += 1
    xcircle = r*np.sin(np.pi*2*kt/360/8)
    ycircle = r*np.cos(np.pi*2*kt/360/8)

    point1 = center + np.array([xcircle, ycircle])

    sline = S_line(env, point0, point1)
    env.line = sline
    env.clear_environment()

    for i, ag in enumerate(env.agents):
        ag.final_v(cohese=cohese, avoid=True, align=align, follow=False, go_point=go_point, go_line=go_line)
        ag.update_velocity()
        ag.update_position()
        ag.draw_history(env.screen)
    env.line.draw()
    env.update_agents()
    env.draw_agents()
    pg.time.delay(int(constants.dt*1000))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                for i in env.agents:
                    i.reset_position()
            if event.key == pg.K_h:
                for ag in env.agents:
                    ag.reset_history()

            if event.key == pg.K_c:
                cohese = not cohese
            if event.key == pg.K_p:
                go_point = not go_point
            if event.key == pg.K_l:
                go_line = not go_line
            if event.key == pg.K_a:
                align = not align
    env.update_environment()