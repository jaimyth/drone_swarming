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

n = 18
x_pos = 200
y_pos = np.linspace(200,600, n)



for i in range(n):
    #ag = Agent_Flock(environment=env, x = random.randint(150, 250), y = random.randint(150, 250), id=get_id())
    ag = Agent_Flock(environment=env, x = y_pos[i]+5*i, y = y_pos[i], id=get_id())
    env.add_agent(ag)

run =  True
cohese = False
go_point = False
go_line = False
align = False
distribute = False

point0 = np.array([400, 400])
point1 = np.array([500, 500])
point2 = np.array([701, 401])
point3 = np.array([501, 351])
line0 = S_line(env, point0, point1)
line1 = S_line(env, point1, point2)
line2 = S_line(env, point2, point3)
line3 = S_line(env, point3, point0)
env.lines = [line0, line1, line2, line3]

''''
point0 = np.array([400, 400])
point1 = np.array([400, 500])
point2 = np.array([475, 550])
point3 = np.array([550, 500])
point4 = np.array([550, 400])
point5 = np.array([475, 300])

line0 = S_line(env, point0, point1)
line1 = S_line(env, point1, point2)
line2 = S_line(env, point2, point3)
line3 = S_line(env, point3, point4)
line4 = S_line(env, point4, point5)
line5 = S_line(env, point5, point0)
env.lines = [line0, line1, line2, line3, line4, line5]
'''
pp = Ppoint(env, 475, 475)
env.ppoints = [pp]

kt = 0
while run:
    t = pg.time.get_ticks()
    kt += 1

    env.clear_environment()

    for i, ag in enumerate(env.agents):
        ag.final_v(cohese=cohese, avoid=True, align=align, follow=False, go_point=go_point, go_line=False, go_lines=go_line, distribute=distribute)
        ag.update_velocity()
        ag.update_position()
        #ag.draw_history(env.screen)

 #   for line in env.lines:
#        line.draw()

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
            if event.key == pg.K_d:
                distribute = not distribute
    env.update_environment()